import sys
import os
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

# ------------------------------------------------------------------
# PATH SETUP
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))

from config.data_connections import get_duckdb_connection
from scripts.transformations.utils.lake_retention import cleanup_old_runs

# ------------------------------------------------------------------
# CONFIGURAÇÕES DO PIPELINE
# ------------------------------------------------------------------
TARGET_TABLE = "abt_base_cmv"
ANCHOR_PATH = "s3://lake/gold/labels_fpd_bureau/**/*.parquet"

RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d")
GOLD_BASE_PATH = f"gold/{TARGET_TABLE}/"
GOLD_PATH = f"s3://lake/{GOLD_BASE_PATH}run_id={RUN_ID}/"

QUALITY_REPORT_PATH = PROJECT_ROOT / "reports" / "observability" / "quality" / "pipeline" / f"gold-{TARGET_TABLE}-quality.log"

MAX_GOLD_RUNS = int(os.getenv("GOLD_MAX_RUNS", 1))

def run():
    con = get_duckdb_connection()
    con.execute("SET preserve_insertion_order = false")
    # Trava de segurança para a VPS
    con.execute("SET memory_limit = '5GB'")
    
    WORK_DB_PATH = f"/mnt/nvme/duckdb_temp/work_{TARGET_TABLE}.db"
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)
    con.execute(f"ATTACH '{WORK_DB_PATH}' AS work_db")

    print("--------------------------------------------------")
    print(f"🚀 Iniciando Gold ABT (Fusão: Perfomance Velha + Inteligência Nova): {TARGET_TABLE}")
    
    # ------------------------------------------------------------------
    # ETAPA 1: AGREGAÇÕES TRANSACIONAIS (COM FEATURES DE VELOCIDADE)
    # ------------------------------------------------------------------
    print("🎯 Etapa 1: Agregando histórico transacional (Geral e Trava 90D)...")

    # 1.1 RECARGA
    con.execute(f"""
        CREATE TABLE work_db.agg_recarga AS
        WITH base_anchor AS (SELECT DISTINCT num_cpf, safra FROM read_parquet('{ANCHOR_PATH}'))
        SELECT 
            b.num_cpf, b.safra,
            -- QTD & VALOR TOTAL
            COUNT(r.val_credito_inserido) as rec_qtd_geral,
            COUNT(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 30) as rec_qtd_l30d,
            COUNT(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60) as rec_qtd_l60d,
            COUNT(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90) as rec_qtd_l90d,
            
            SUM(r.val_credito_inserido) as rec_vlr_total_geral,
            SUM(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 30) as rec_vlr_total_l30d,
            SUM(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60) as rec_vlr_total_l60d,
            SUM(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90) as rec_vlr_total_l90d,
            
            -- TENDÊNCIA DE RECARGA (Mês atual vs Média Histórica)
            (SUM(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 30)) 
            / NULLIF((SUM(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90)) / 3.0, 0) 
            as rec_tendencia_vlr_l30_l90,

            -- SOS: Cliente sem liquidez financeira
            COUNT(r.valor_sos) FILTER (WHERE r.flag_sos = true) as rec_qtd_sos_geral,
            COUNT(r.valor_sos) FILTER (WHERE r.flag_sos = true AND r.dat_insercao_credito >= b.safra - 90) as rec_qtd_sos_l90d,
            SUM(r.valor_sos) FILTER (WHERE r.flag_sos = true AND r.dat_insercao_credito >= b.safra - 90) as rec_vlr_sos_l90d,

            -- Canal de Pagamento: Digital vs Fisico
            COUNT(r.val_credito_inserido) FILTER (WHERE LOWER(r.dsc_canal_aquisicao) LIKE '%pix%' OR LOWER(r.dsc_canal_aquisicao) LIKE '%mercado pago%') as rec_qtd_canais_digitais_geral,
            COUNT(r.val_credito_inserido) FILTER (WHERE (LOWER(r.dsc_canal_aquisicao) LIKE '%pix%' OR LOWER(r.dsc_canal_aquisicao) LIKE '%mercado pago%') AND r.dat_insercao_credito >= b.safra - 90) as rec_qtd_canais_digitais_l90d,

            -- RECENCIA E ATIVIDADE
            DATE_DIFF('day', MAX(r.dat_insercao_credito), b.safra) as rec_dias_desde_ultima,
            STDDEV(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90) as rec_vlr_std_l90d,
            
            -- Engagement de Bônus e Plano
            SUM(r.val_bonus) as rec_vlr_bonus_geral,
            SUM(r.val_bonus) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90) as rec_vlr_bonus_l90d,
            COUNT(r.val_credito_inserido) FILTER (WHERE LOWER(r.dsc_plano_tarifacao) LIKE '%controle%') as rec_qtd_plano_controle_geral,

            -- Volatilidade e Variação
            STDDEV(r.val_credito_inserido) / NULLIF(AVG(r.val_credito_inserido), 0) AS rec_volatilidade_ticket,
            MAX(r.val_credito_inserido) / NULLIF(SUM(r.val_credito_inserido), 0) AS rec_indice_concentracao,
            
            -- Status Específicos e Plataformas
            COUNT(r.val_credito_inserido) FILTER (WHERE r.cod_status_plataforma = 'A') / NULLIF(COUNT(r.val_credito_inserido), 0) AS rec_share_status_ativo,
            COUNT(r.val_credito_inserido) FILTER (WHERE r.cod_plataforma_atu = 'AUTOC') AS rec_qtd_plat_autoc,
            COUNT(r.val_credito_inserido) FILTER (WHERE r.dsc_grupo_cartao_wpp = 'Rec.Online') / NULLIF(COUNT(r.val_credito_inserido), 0) AS rec_taxa_cartao_online,
            
            LEAST(100, GREATEST(0,
                COALESCE(COUNT(r.val_credito_inserido) FILTER (WHERE r.cod_plataforma_atu IN ('CTLFC', 'FLEXD')) / NULLIF(COUNT(r.val_credito_inserido), 0), 0) * 30 +
                COALESCE(COUNT(r.val_credito_inserido) FILTER (WHERE r.cod_status_plataforma IN ('ZB1', 'ZB2')) / NULLIF(COUNT(r.val_credito_inserido), 0), 0) * 25 +
                LEAST(1, COALESCE(COUNT(r.valor_sos) FILTER (WHERE r.flag_sos = true) / NULLIF(COUNT(r.val_credito_inserido), 0), 0) * 3) * 20 +
                LEAST(1, COALESCE(STDDEV(r.val_credito_inserido) / NULLIF(AVG(r.val_credito_inserido), 0), 0)) * 15 +
                LEAST(1, COALESCE(MAX(r.val_credito_inserido) / NULLIF(SUM(r.val_credito_inserido), 0), 0)) * 10
            )) AS rec_indice_estresse_financeiro
            
        FROM base_anchor b
        LEFT JOIN read_parquet('s3://lake/silver/recarga/**/*.parquet') r 
            ON b.num_cpf = r.num_cpf AND r.dat_insercao_credito < b.safra
        GROUP BY 1, 2
    """)

    # 1.2 PAGAMENTO
    con.execute(f"""
        CREATE TABLE work_db.agg_pagamento AS
        WITH base_anchor AS (SELECT DISTINCT num_cpf, safra FROM read_parquet('{ANCHOR_PATH}'))
        SELECT 
            b.num_cpf, b.safra,
            -- COMPORTAMENTO FINANCEIRO
            SUM(p.val_pagamento_fatura) as pag_vlr_total_geral,
            SUM(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90) as pag_vlr_total_l90d,
            
            SUM(p.val_pagamento_fatura) / NULLIF(COUNT(DISTINCT p.seq_fatura), 0) as pag_ticket_medio_geral,
            SUM(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90) / NULLIF(COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90), 0) as pag_ticket_medio_l90d,
            
            COUNT(DISTINCT p.seq_fatura) as pag_qtd_faturas_geral,
            COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90) as pag_qtd_faturas_l90d,
            
            -- MICRO-ATRASOS E DEBITO DIRETO
            AVG(DATE_DIFF('day', p.dat_vencimento_credito, p.dat_atividade_credito)) FILTER (WHERE p.dat_atividade_credito > p.dat_vencimento_credito) as pag_media_dias_atraso_geral,
            AVG(DATE_DIFF('day', p.dat_vencimento_credito, p.dat_atividade_credito)) FILTER (WHERE p.dat_atividade_credito > p.dat_vencimento_credito AND p.dat_status_fatura >= b.safra - 90) as pag_media_dias_atraso_l90d,
            
            MAX(DATE_DIFF('day', p.dat_vencimento_credito, p.dat_atividade_credito)) FILTER (WHERE p.dat_atividade_credito > p.dat_vencimento_credito) as pag_max_dias_atraso_geral,

            COUNT(p.val_pagamento_fatura) FILTER (WHERE p.cod_forma_pagamento IN ('DD', 'D')) as pag_qtd_debito_direto_geral,
            COUNT(p.val_pagamento_fatura) FILTER (WHERE p.cod_forma_pagamento IN ('DD', 'D') AND p.dat_status_fatura >= b.safra - 90) as pag_qtd_debito_direto_l90d,

            -- Saúde financeira (Juros e Volatilidade)
            COUNT(p.val_juros_multas_item) FILTER (WHERE p.val_juros_multas_item > 0) / NULLIF(COUNT(DISTINCT p.seq_fatura), 0) as pag_share_faturas_com_juros_geral,
            COALESCE(COUNT(p.val_juros_multas_item) FILTER (WHERE p.val_juros_multas_item > 0 AND p.dat_status_fatura >= b.safra - 90) / NULLIF(COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90), 0), 0) as pag_share_faturas_com_juros_l90d,
            
            DATE_DIFF('day', MAX(p.dat_status_fatura), b.safra) as pag_dias_desde_ultimo_pagamento,

            STDDEV(p.val_pagamento_fatura) AS pag_vlr_std_geral,
            STDDEV(p.val_pagamento_fatura) / NULLIF(AVG(p.val_pagamento_fatura), 0) AS pag_instabilidade_pagamento,
            COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.ind_status_fatura = 'O') / NULLIF(COUNT(DISTINCT p.seq_fatura), 0) AS pag_taxa_fatura_aberta,
            
            --  FATOR DE RISCO (SCORE) 
            LEAST(100, GREATEST(0,
                COALESCE((COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.ind_status_fatura = 'O')) / NULLIF(COUNT(p.val_pagamento_fatura), 0), 0) * 25 +
                LEAST(1, COALESCE(SUM(p.val_juros_multas_item) / NULLIF(SUM(p.val_pagamento_fatura), 0), 0) * 5) * 25 +
                COALESCE((COUNT(p.val_pagamento_fatura) FILTER (WHERE p.ind_status_pagamento = 'B')) / NULLIF(COUNT(p.val_pagamento_fatura), 0), 0) * 20 +
                LEAST(1, COALESCE(STDDEV(p.val_pagamento_fatura) / NULLIF(AVG(p.val_pagamento_fatura), 0), 0)) * 15 +
                CASE WHEN COUNT(p.val_multa_equip_item) FILTER (WHERE p.val_multa_equip_item > 0) > 0 THEN 15 ELSE 0 END
            )) AS pag_fator_risco_comportamental

        FROM base_anchor b
        LEFT JOIN read_parquet('s3://lake/silver/pagamento/**/*.parquet') p 
            ON b.num_cpf = p.num_cpf AND p.dat_status_fatura < b.safra
        GROUP BY 1, 2
    """)

    # 1.3 ATRASO
    con.execute(f"""
        CREATE TABLE work_db.agg_atraso AS
        WITH base_anchor AS (SELECT DISTINCT num_cpf, safra FROM read_parquet('{ANCHOR_PATH}'))
        SELECT 
            b.num_cpf, b.safra,
            -- EXPOSICAO A RISCO
            SUM(a.val_fat_aberto) as atr_vlr_acumulado_geral,
            SUM(a.val_fat_aberto) FILTER (WHERE a.dat_referencia >= b.safra - 90) as atr_vlr_acumulado_l90d,
            
            MAX(a.val_fat_aberto) as atr_vlr_max_geral,
            
            COUNT(DISTINCT a.num_fatura_hash) as atr_qtd_faturas_atrasadas_geral,
            COUNT(DISTINCT a.num_fatura_hash) FILTER (WHERE a.dat_referencia >= b.safra - 90) as atr_qtd_faturas_atrasadas_l90d,
            
            DATE_DIFF('day', MAX(a.dat_referencia), b.safra) as atr_dias_desde_ultimo_atraso,

            -- GRAVIDADE E PREJUIZO
            MAX(CAST(a.dw_faixa_aging_divida AS INTEGER)) as atr_max_aging_divida_geral,
            MAX(CAST(a.dw_faixa_aging_divida AS INTEGER)) FILTER (WHERE a.dat_referencia >= b.safra - 90) as atr_max_aging_divida_l90d,
            
            COUNT(a.num_fatura_hash) FILTER (WHERE a.ind_pdd = 'S') as atr_qtd_pdd_geral,
            COUNT(a.num_fatura_hash) FILTER (WHERE a.ind_wo IN ('W', 'S')) as atr_qtd_wo_geral,
            COUNT(a.num_fatura_hash) FILTER (WHERE a.ind_fraude = 'S') as atr_qtd_fraude_geral,

            -- Proporção de dívida severa (Aging alto) em relação à média do cliente
            MAX(CAST(a.dw_faixa_aging_divida AS INTEGER)) / NULLIF(AVG(CAST(a.dw_faixa_aging_divida AS INTEGER)), 0) AS atr_fator_cronico,

            -- INDICE DE GRAVIDADE 
            LEAST(100, GREATEST(0,
                COALESCE(COUNT(a.num_fatura_hash) FILTER (WHERE a.ind_wo IN ('W', 'S')) / NULLIF(COUNT(DISTINCT a.num_fatura_hash), 0), 0) * 35 +
                COALESCE(COUNT(a.num_fatura_hash) FILTER (WHERE a.ind_pdd = 'S') / NULLIF(COUNT(DISTINCT a.num_fatura_hash), 0), 0) * 25 +
                COALESCE(COUNT(a.num_fatura_hash) FILTER (WHERE a.ind_fraude = 'S') / NULLIF(COUNT(DISTINCT a.num_fatura_hash), 0), 0) * 20 +
                COALESCE(COUNT(a.num_fatura_hash) FILTER (WHERE CAST(a.dw_faixa_aging_divida AS INTEGER) > 2) / NULLIF(COUNT(DISTINCT a.num_fatura_hash), 0), 0) * 20
            )) AS atr_indice_gravidade_historica
            
        FROM base_anchor b
        LEFT JOIN read_parquet('s3://lake/silver/atraso/**/*.parquet') a 
            ON b.num_cpf = a.num_cpf AND a.dat_referencia < b.safra
        GROUP BY 1, 2
    """)

# ------------------------------------------------------------------
    # ETAPA 2: MASTER JOIN E EXTRACAO DE CADASTRAIS + 11 GOLDEN FEATURES
    # ------------------------------------------------------------------
    print("🔗 Etapa 2: Executando Master Join e Extração de Cadastrais...")

    def get_select_prefixed(table_path, prefix, skip_cols):
        cols = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{table_path}')").df()['column_name'].tolist()
        return ", ".join([f'"{c}" AS "{prefix}_{c}"' for c in cols if c not in skip_cols])

    keys_to_skip = ['num_cpf', 'safra', 'prod', 'fpd', 'flag_instalacao', 'ano_mes', 'ingestion_ts', 'run_id']
    
    bur_select = get_select_prefixed('s3://lake/silver/score_bureau_movel/**/*.parquet', 'bur', keys_to_skip)
    cad_select = get_select_prefixed('s3://lake/silver/dados_cadastrais/**/*.parquet', 'cad', keys_to_skip)
    tel_select = get_select_prefixed('s3://lake/silver/telco/**/*.parquet', 'tel', keys_to_skip)

    con.execute(f"""
        CREATE TABLE work_db.gold_step1 AS
        WITH 
        bur AS (SELECT num_cpf, safra, prod, {bur_select} FROM read_parquet('s3://lake/silver/score_bureau_movel/**/*.parquet')),
        cad AS (SELECT num_cpf, safra, prod, {cad_select} FROM read_parquet('s3://lake/silver/dados_cadastrais/**/*.parquet')),
        tel AS (SELECT num_cpf, safra, prod, {tel_select} FROM read_parquet('s3://lake/silver/telco/**/*.parquet'))
        
        SELECT 
            -- Identificadores base
            a.num_cpf, a.safra, a.prod, a.fpd, a.flag_instalacao,

            -- Colunas transacionais 
            r.* EXCLUDE (num_cpf, safra),
            p.* EXCLUDE (num_cpf, safra),
            atr.* EXCLUDE (num_cpf, safra),

            -- Scores do Bureau
            b.* EXCLUDE (num_cpf, safra, prod),

            -- Telco Bruto
            t.* EXCLUDE (num_cpf, safra, prod),

            -- DADOS CADASTRAIS (COMPLETOS)
            c.* EXCLUDE (num_cpf, safra, prod),

            DATE_DIFF('year', c.cad_datadenascimento, a.safra) AS idade,
            DATE_DIFF('day', c.cad_var_12, a.safra) AS tempo_conta_dias,

            CASE WHEN c.cad_var_25 ILIKE '%AUX_EMRG%' THEN 1 ELSE 0 END AS flag_auxilio_emergencial,
            CASE WHEN c.cad_var_25 ILIKE '%BOLSA_FAMILIA%' OR c.cad_var_23 = 'BOLSA_FAMILIA' THEN 1 ELSE 0 END AS flag_bolsa_familia,
            CASE WHEN c.cad_var_25 ILIKE '%APOSENTADO%' OR c.cad_var_18 = 'APOSENTADO' THEN 1 ELSE 0 END AS flag_aposentado,
            CASE WHEN c.cad_var_25 ILIKE '%FUNC_PRIVADO%' OR c.cad_var_21 = 'FUNC_PRIVADO' THEN 1 ELSE 0 END AS flag_funcionario_privado,
            CASE WHEN c.cad_statusrf IN ('NULA', 'SUSPENSA', 'TITULAR FALECIDO') THEN 1 ELSE 0 END AS cad_flag_statusrf_irregular,


            -- 1. Completude Cadastral
            (CASE WHEN c.cad_var_02 IS NOT NULL THEN 1 ELSE 0 END + 
             CASE WHEN c.cad_var_04 IS NOT NULL THEN 1 ELSE 0 END + 
             CASE WHEN c.cad_var_05 IS NOT NULL THEN 1 ELSE 0 END + 
             CASE WHEN c.cad_var_16 IS NOT NULL THEN 1 ELSE 0 END) AS cad_completude,
            
            -- 2. Índice Estabilidade
            (CASE WHEN c.cad_var_25 ILIKE '%FUNC_PRIVADO%' OR c.cad_var_21 = 'FUNC_PRIVADO' THEN 1 ELSE 0 END + 
             CASE WHEN c.cad_var_25 ILIKE '%APOSENTADO%' OR c.cad_var_18 = 'APOSENTADO' THEN 1 ELSE 0 END) AS cad_indice_estabilidade,
            
            -- 3. Bureau x Estabilidade
            COALESCE(b.bur_score_02, 0) * (1 + ((
                CASE WHEN c.cad_var_25 ILIKE '%FUNC_PRIVADO%' OR c.cad_var_21 = 'FUNC_PRIVADO' THEN 1 ELSE 0 END + 
                CASE WHEN c.cad_var_25 ILIKE '%APOSENTADO%' OR c.cad_var_18 = 'APOSENTADO' THEN 1 ELSE 0 END
            ) * 0.15)) AS cad_bureau_x_estabilidade,

            -- 4. Ratio SOS (Trava 90 dias)
            COALESCE(r.rec_vlr_sos_l90d, 0) / NULLIF(COALESCE(r.rec_vlr_total_l90d, 0), 0) AS rec_dependencia_sos,
            
            -- 5. Share Digital (Trava 90 dias)
            COALESCE(r.rec_qtd_canais_digitais_l90d, 0) / NULLIF(COALESCE(r.rec_qtd_l90d, 0), 0) AS rec_share_digital,
            
            -- 6. Share Bonus (Trava 90 dias)
            COALESCE(r.rec_vlr_bonus_l90d, 0) / NULLIF(COALESCE(r.rec_vlr_total_l90d, 0), 0) AS rec_share_bonus,

            -- 7. Intensidade de Atraso (Trava 90 dias)
            COALESCE(atr.atr_vlr_acumulado_l90d, 0) / NULLIF(COALESCE(p.pag_ticket_medio_l90d, 0), 0) AS atr_intensidade,
            
            -- 8. Esforço de Pagamento (Trava 90 dias)
            COALESCE(atr.atr_vlr_acumulado_l90d, 0) / NULLIF(COALESCE(p.pag_vlr_total_l90d, 0), 0) AS pag_esforco,
            
            -- 9. Taxa de Falha (Trava 90 dias)
            COALESCE(atr.atr_qtd_faturas_atrasadas_l90d, 0) / NULLIF(COALESCE(atr.atr_qtd_faturas_atrasadas_l90d, 0) + COALESCE(p.pag_qtd_faturas_l90d, 0), 0) AS pag_taxa_falha,
            
            -- 10. Misto Recarga vs Pagamento (Geral)
            COALESCE(r.rec_vlr_total_geral, 0) / NULLIF(COALESCE(p.pag_vlr_total_geral, 0), 0) AS pag_vs_recarga_total,
            
            -- 11. Severidade Juros (Trava 90 dias)
            COALESCE(p.pag_share_faturas_com_juros_l90d, 0) * COALESCE(p.pag_media_dias_atraso_l90d, 0) AS pag_severidade_juros,

            -- Metadados finais
            '{RUN_ID}' AS run_id,
            now() AS ingestion_ts,
            a.ano_mes
            
        FROM read_parquet('{ANCHOR_PATH}') a
        LEFT JOIN bur b ON a.num_cpf = b.num_cpf AND a.safra = b.safra AND a.prod = b.prod
        LEFT JOIN cad c ON a.num_cpf = c.num_cpf AND a.safra = c.safra AND a.prod = c.prod
        LEFT JOIN tel t ON a.num_cpf = t.num_cpf AND a.safra = t.safra AND a.prod = t.prod
        LEFT JOIN work_db.agg_recarga r ON a.num_cpf = r.num_cpf AND a.safra = r.safra
        LEFT JOIN work_db.agg_pagamento p ON a.num_cpf = p.num_cpf AND a.safra = p.safra
        LEFT JOIN work_db.agg_atraso atr ON a.num_cpf = atr.num_cpf AND a.safra = atr.safra
    """)

    # ------------------------------------------------------------------
    # ETAPA 3: AUDITORIA DE INTEGRIDADE E RELATÓRIO TÉCNICO
    # ------------------------------------------------------------------
    print("📊 Etapa 3: Gerando métricas de integridade e cobertura...")
    
    stats = con.execute("SELECT COUNT(*), COUNT(DISTINCT num_cpf) FROM work_db.gold_step1").fetchone()
    total_rows, total_cpfs = stats
    
    cols_ignorar = ['num_cpf', 'safra', 'prod', 'fpd', 'run_id', 'ingestion_ts', 'ano_mes']
    todas_as_cols = con.execute("DESCRIBE work_db.gold_step1").df()['column_name'].tolist()
    features_reais = [c for c in todas_as_cols if c not in cols_ignorar]
    num_features = len(features_reais)

    fontes = {
        "Bureau Score":        {"col": "bur_score_02",      "tipo": "Master Join"}, 
        "Dados Cadastrais":    {"col": "idade",             "tipo": "Processado"}, 
        "Telco Features":      {"col": "tel_var_78",        "tipo": "Master Join"}, 
        "Histórico Recarga":   {"col": "rec_qtd_geral",     "tipo": "Agregação"},
        "Histórico Pagamento": {"col": "pag_vlr_total_geral", "tipo": "Agregação"},
        "Histórico Atraso":    {"col": "atr_vlr_max_geral",   "tipo": "Agregação"}
    }

    col_list = ", ".join([f"COUNT({cfg['col']}) AS count_{i}" for i, cfg in enumerate(fontes.values())])
    counts_res = con.execute(f"SELECT {col_list} FROM work_db.gold_step1").fetchone()
    
    report_log = f"📋 GOLD ABT REPORT - {TARGET_TABLE} | RUN: {RUN_ID}\n"
    report_log += "="*100 + "\n"
    report_log += f"🏆 STATUS GERAL: ✅ SUCCESS | VARIÁVEIS: {num_features} features | REGISTROS: {total_rows:,} | CPFs ÚNICOS: {total_cpfs:,}\n".replace(",", ".")
    report_log += "="*100 + "\n\n"
    report_log += "INTEGRIDADE E COBERTURA DE DADOS:\n"
    report_log += "-"*100 + "\n"
    report_log += f"{'FONTE DE DADOS':<23} | {'TIPO':<12} | {'STATUS':<6} | {'PREENCHIMENTO (%)':<17} | {'INFO ADICIONAL'}\n"
    report_log += "-"*100 + "\n"

    for i, (nome, cfg) in enumerate(fontes.items()):
        present_count = counts_res[i]
        perc = (present_count / total_rows * 100) if total_rows > 0 else 0.0
        
        if cfg['tipo'] == "Master Join":
            status = "PASS" if perc > 95 else "INFO"
            orfãos = total_rows - present_count
            info = f"{orfãos:,} registros órfãos".replace(",", ".")
        else:
            status = "PASS"
            obs = {
                "Histórico Recarga":   "CPFs com atividade de recarga",
                "Histórico Pagamento": "CPFs com evidência de pagamento",
                "Histórico Atraso":    "CPFs com histórico de atraso",
                "Dados Cadastrais":    "CPFs com Info na Receita/Cadastral"
            }
            info = obs.get(nome, "")
        report_log += f"{nome:<23} | {cfg['tipo']:<12} | {status:<6} | {perc:>15.1f}% | {info}\n"
    
    report_log += "-"*100 + "\n"
    print(report_log)
    
    os.makedirs(QUALITY_REPORT_PATH.parent, exist_ok=True)
    with open(QUALITY_REPORT_PATH, "w") as f: 
        f.write(report_log)

    con.execute(f"COPY (SELECT * FROM work_db.gold_step1) TO '{GOLD_PATH}' (FORMAT PARQUET, PARTITION_BY (ano_mes), OVERWRITE_OR_IGNORE 1)")    
    
    con.execute("DETACH work_db")
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)
    
    cleanup_old_runs(bucket="lake", base_path=GOLD_BASE_PATH, max_runs=MAX_GOLD_RUNS, protect_run_id=RUN_ID)
    print(f"🏁 ABT persistida em: {GOLD_PATH}")

if __name__ == "__main__":
    run()