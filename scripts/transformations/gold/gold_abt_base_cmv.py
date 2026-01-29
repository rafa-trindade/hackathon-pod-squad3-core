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
    
    WORK_DB_PATH = f"/mnt/nvme/duckdb_temp/work_{TARGET_TABLE}.db"
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)
    con.execute(f"ATTACH '{WORK_DB_PATH}' AS work_db")

    print("--------------------------------------------------")
    print(f"🏆 Iniciando Gold ABT: {TARGET_TABLE}")
    
    # ------------------------------------------------------------------
    # ETAPA 1: AGREGAÇÕES TRANSACIONAIS (30, 60, 90 + TOTAL)
    # ------------------------------------------------------------------
    print("🎯 Etapa 1: Agregando histórico transacional...")

    # 1.1 RECARGA
    con.execute(f"""
        CREATE TABLE work_db.agg_recarga AS
        WITH base_anchor AS (SELECT DISTINCT num_cpf, safra FROM read_parquet('{ANCHOR_PATH}'))
        SELECT 
            b.num_cpf, b.safra,
            -- QTD
            COUNT(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 30) as rec_qtd_l30d,
            COUNT(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60) as rec_qtd_l60d,
            COUNT(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90) as rec_qtd_l90d,
            COUNT(r.val_credito_inserido) as rec_qtd_geral,
            -- VLR TOTAL
            SUM(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 30) as rec_vlr_total_l30d,
            SUM(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60) as rec_vlr_total_l60d,
            SUM(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90) as rec_vlr_total_l90d,
            SUM(r.val_credito_inserido) as rec_vlr_total_geral,
            -- VLR AVG
            AVG(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 30) as rec_vlr_avg_l30d,
            AVG(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60) as rec_vlr_avg_l60d,
            AVG(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90) as rec_vlr_avg_l90d,
            AVG(r.val_credito_inserido) as rec_vlr_avg_geral,
            -- VLR MIN
            MIN(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 30) as rec_vlr_min_l30d,
            MIN(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60) as rec_vlr_min_l60d,
            MIN(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90) as rec_vlr_min_l90d,
            MIN(r.val_credito_inserido) as rec_vlr_min_geral,
            -- VLR MAX
            MAX(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 30) as rec_vlr_max_l30d,
            MAX(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60) as rec_vlr_max_l60d,
            MAX(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90) as rec_vlr_max_l90d,
            MAX(r.val_credito_inserido) as rec_vlr_max_geral,
            -- DATAS E CANAIS
            MIN(r.dat_insercao_credito) as rec_dat_primeira,
            MAX(r.dat_insercao_credito) as rec_dat_ultima,
            COUNT(DISTINCT r.cod_canal_aquisicao) as rec_qtd_canais_distintos,

            -- RECENCIA
            DATE_DIFF('day', MAX(r.dat_insercao_credito), b.safra) as rec_dias_desde_ultima,
            DATE_DIFF('day', MIN(r.dat_insercao_credito), b.safra) as rec_dias_desde_primeira,

            -- VLR STD
            STDDEV(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 30) as rec_vlr_std_l30d,
            STDDEV(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60) as rec_vlr_std_l60d,
            STDDEV(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90) as rec_vlr_std_l90d,
            STDDEV(r.val_credito_inserido) as rec_vlr_std_geral,

            -- VLR COEF VAR
            STDDEV(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 30)
            / NULLIF(AVG(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 30), 0)
            as rec_vlr_coef_var_l30d,

            STDDEV(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60)
            / NULLIF(AVG(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60), 0)
            as rec_vlr_coef_var_l60d,

            STDDEV(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90)
            / NULLIF(AVG(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90), 0)
            as rec_vlr_coef_var_l90d,

            -- RAZOES QTD
            COUNT(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 30)
            / NULLIF(COUNT(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60), 0)
            as rec_ratio_qtd_l30d_l60d,

            COUNT(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60)
            / NULLIF(COUNT(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90), 0)
            as rec_ratio_qtd_l60d_l90d,

            -- RAZOES VLR
            SUM(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 30)
            / NULLIF(SUM(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60), 0)
            as rec_ratio_vlr_l30d_l60d,

            SUM(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60)
            / NULLIF(SUM(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90), 0)
            as rec_ratio_vlr_l60d_l90d,

            -- FLAGS
            CASE WHEN COUNT(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 30) = 0
                THEN 1 ELSE 0 END as rec_flag_sem_recarga_l30d,

            CASE WHEN COUNT(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 60) = 0
                THEN 1 ELSE 0 END as rec_flag_sem_recarga_l60d,

            CASE WHEN COUNT(r.val_credito_inserido) FILTER (WHERE r.dat_insercao_credito >= b.safra - 90) = 0
                THEN 1 ELSE 0 END as rec_flag_sem_recarga_l90d


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
            -- VLR TOTAL
            SUM(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 30) as pag_vlr_total_l30d,
            SUM(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 60) as pag_vlr_total_l60d,
            SUM(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90) as pag_vlr_total_l90d,
            SUM(p.val_pagamento_fatura) as pag_vlr_total_geral,
            -- VLR AVG
            AVG(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 30) as pag_vlr_avg_l30d,
            AVG(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 60) as pag_vlr_avg_l60d,
            AVG(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90) as pag_vlr_avg_l90d,
            AVG(p.val_pagamento_fatura) as pag_vlr_avg_geral,
            -- VLR MIN
            MIN(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 30) as pag_vlr_min_l30d,
            MIN(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 60) as pag_vlr_min_l60d,
            MIN(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90) as pag_vlr_min_l90d,
            MIN(p.val_pagamento_fatura) as pag_vlr_min_geral,
            -- VLR MAX
            MAX(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 30) as pag_vlr_max_l30d,
            MAX(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 60) as pag_vlr_max_l60d,
            MAX(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90) as pag_vlr_max_l90d,
            MAX(p.val_pagamento_fatura) as pag_vlr_max_geral,
            -- QTD FATURAS
            COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 30) as pag_qtd_faturas_l30d,
            COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 60) as pag_qtd_faturas_l60d,
            COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90) as pag_qtd_faturas_l90d,
            COUNT(DISTINCT p.seq_fatura) as pag_qtd_faturas_geral,
            COUNT(p.val_juros_multas_item) FILTER (WHERE p.val_juros_multas_item > 0) as pag_qtd_vezes_com_juros,
                
            -- RECENCIA
            DATE_DIFF('day', MAX(p.dat_status_fatura), b.safra) as pag_dias_desde_ultimo_pagamento,

            -- TICKET MEDIO
            SUM(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 30)
            / NULLIF(COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 30), 0)
            as pag_ticket_medio_l30d,

            SUM(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 60)
            / NULLIF(COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 60), 0)
            as pag_ticket_medio_l60d,

            SUM(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90)
            / NULLIF(COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90), 0)
            as pag_ticket_medio_l90d,

            SUM(p.val_pagamento_fatura)
            / NULLIF(COUNT(DISTINCT p.seq_fatura), 0)
            as pag_ticket_medio_geral,

            -- SHARE JUROS
            COUNT(p.val_juros_multas_item) FILTER (
                WHERE p.val_juros_multas_item > 0
                AND p.dat_status_fatura >= b.safra - 30
            ) / NULLIF(COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 30), 0)
            as pag_share_faturas_com_juros_l30d,

            COUNT(p.val_juros_multas_item) FILTER (
                WHERE p.val_juros_multas_item > 0
                AND p.dat_status_fatura >= b.safra - 60
            ) / NULLIF(COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 60), 0)
            as pag_share_faturas_com_juros_l60d,

            COUNT(p.val_juros_multas_item) FILTER (
                WHERE p.val_juros_multas_item > 0
                AND p.dat_status_fatura >= b.safra - 90
            ) / NULLIF(COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90), 0)
            as pag_share_faturas_com_juros_l90d,

            COUNT(p.val_juros_multas_item) FILTER (WHERE p.val_juros_multas_item > 0)
            / NULLIF(COUNT(DISTINCT p.seq_fatura), 0)
            as pag_share_faturas_com_juros_geral,

            -- VLR STD
            STDDEV(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 30) as pag_vlr_std_l30d,
            STDDEV(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 60) as pag_vlr_std_l60d,
            STDDEV(p.val_pagamento_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90) as pag_vlr_std_l90d,

            -- FLAGS
            CASE WHEN COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 30) = 0
                THEN 1 ELSE 0 END as pag_flag_sem_pagamento_l30d,

            CASE WHEN COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 60) = 0
                THEN 1 ELSE 0 END as pag_flag_sem_pagamento_l60d,

            CASE WHEN COUNT(DISTINCT p.seq_fatura) FILTER (WHERE p.dat_status_fatura >= b.safra - 90) = 0
                THEN 1 ELSE 0 END as pag_flag_sem_pagamento_l90d


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
            -- VLR MAX
            MAX(a.val_fat_aberto) FILTER (WHERE a.dat_referencia >= b.safra - 30) as atr_vlr_max_l30d,
            MAX(a.val_fat_aberto) FILTER (WHERE a.dat_referencia >= b.safra - 60) as atr_vlr_max_l60d,
            MAX(a.val_fat_aberto) FILTER (WHERE a.dat_referencia >= b.safra - 90) as atr_vlr_max_l90d,
            MAX(a.val_fat_aberto) as atr_vlr_max_geral,
            -- VLR ACUMULADO
            SUM(a.val_fat_aberto) FILTER (WHERE a.dat_referencia >= b.safra - 30) as atr_vlr_acumulado_l30d,
            SUM(a.val_fat_aberto) FILTER (WHERE a.dat_referencia >= b.safra - 60) as atr_vlr_acumulado_l60d,
            SUM(a.val_fat_aberto) FILTER (WHERE a.dat_referencia >= b.safra - 90) as atr_vlr_acumulado_l90d,
            SUM(a.val_fat_aberto) as atr_vlr_acumulado_geral,
            -- QTD FATURAS
            COUNT(DISTINCT a.num_fatura_hash) FILTER (WHERE a.dat_referencia >= b.safra - 30) as atr_qtd_faturas_atrasadas_l30d,
            COUNT(DISTINCT a.num_fatura_hash) FILTER (WHERE a.dat_referencia >= b.safra - 60) as atr_qtd_faturas_atrasadas_l60d,
            COUNT(DISTINCT a.num_fatura_hash) FILTER (WHERE a.dat_referencia >= b.safra - 90) as atr_qtd_faturas_atrasadas_l90d,
            COUNT(DISTINCT a.num_fatura_hash) as atr_qtd_faturas_atrasadas_geral,
            MAX(a.dat_referencia) as atr_dat_ultima_ref,

            -- RECENCIA
            DATE_DIFF('day', MAX(a.dat_referencia), b.safra) as atr_dias_desde_ultimo_atraso,

            -- TICKET MEDIO
            SUM(a.val_fat_aberto) FILTER (WHERE a.dat_referencia >= b.safra - 30)
            / NULLIF(COUNT(DISTINCT a.num_fatura_hash) FILTER (WHERE a.dat_referencia >= b.safra - 30), 0)
            as atr_ticket_medio_l30d,

            SUM(a.val_fat_aberto) FILTER (WHERE a.dat_referencia >= b.safra - 60)
            / NULLIF(COUNT(DISTINCT a.num_fatura_hash) FILTER (WHERE a.dat_referencia >= b.safra - 60), 0)
            as atr_ticket_medio_l60d,

            SUM(a.val_fat_aberto) FILTER (WHERE a.dat_referencia >= b.safra - 90)
            / NULLIF(COUNT(DISTINCT a.num_fatura_hash) FILTER (WHERE a.dat_referencia >= b.safra - 90), 0)
            as atr_ticket_medio_l90d,

            SUM(a.val_fat_aberto)
            / NULLIF(COUNT(DISTINCT a.num_fatura_hash), 0)
            as atr_ticket_medio_geral,

            -- PERSISTENCIA
            CASE WHEN COUNT(DISTINCT a.num_fatura_hash) FILTER (WHERE a.dat_referencia >= b.safra - 30) >= 2
                THEN 1 ELSE 0 END as atr_flag_recorrente_l30d,

            CASE WHEN COUNT(DISTINCT a.num_fatura_hash) FILTER (WHERE a.dat_referencia >= b.safra - 60) >= 2
                THEN 1 ELSE 0 END as atr_flag_recorrente_l60d,

            CASE WHEN COUNT(DISTINCT a.num_fatura_hash) FILTER (WHERE a.dat_referencia >= b.safra - 90) >= 2
                THEN 1 ELSE 0 END as atr_flag_recorrente_l90d,

            -- FLAGS
            CASE WHEN COUNT(DISTINCT a.num_fatura_hash) FILTER (WHERE a.dat_referencia >= b.safra - 30) > 0
                THEN 1 ELSE 0 END as atr_flag_atraso_l30d,

            CASE WHEN COUNT(DISTINCT a.num_fatura_hash) FILTER (WHERE a.dat_referencia >= b.safra - 60) > 0
                THEN 1 ELSE 0 END as atr_flag_atraso_l60d,

            CASE WHEN COUNT(DISTINCT a.num_fatura_hash) FILTER (WHERE a.dat_referencia >= b.safra - 90) > 0
                THEN 1 ELSE 0 END as atr_flag_atraso_l90d

                
        FROM base_anchor b
        LEFT JOIN read_parquet('s3://lake/silver/atraso/**/*.parquet') a 
            ON b.num_cpf = a.num_cpf AND a.dat_referencia < b.safra
        GROUP BY 1, 2
    """)

    # ------------------------------------------------------------------
    # ETAPA 2: MASTER JOIN
    # ------------------------------------------------------------------
    print("🔗 Etapa 2: Executando Master Join...")

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

            -- Colunas transacionais (Agregados)
            r.* EXCLUDE (num_cpf, safra),
            p.* EXCLUDE (num_cpf, safra),
            atr.* EXCLUDE (num_cpf, safra),

            -- Colunas estáticas na ordem: BUR -> CAD -> TEL
            b.* EXCLUDE (num_cpf, safra, prod),
            c.* EXCLUDE (num_cpf, safra, prod),
            t.* EXCLUDE (num_cpf, safra, prod),

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
    # ETAPA 3: PERSISTÊNCIA E RELATÓRIO
    # ------------------------------------------------------------------
    stats = con.execute("SELECT COUNT(*), COUNT(DISTINCT num_cpf) FROM work_db.gold_step1").fetchone()
    num_colunas = con.execute("SELECT COUNT(*) FROM (DESCRIBE work_db.gold_step1)").fetchone()[0]

    report_log = f"""
📋 RELATÓRIO TÉCNICO ABT - {TARGET_TABLE} | RUN: {RUN_ID}
{"="*65}
✅ Status:              ABT Gerada com Sucesso
📊 Variáveis:           {num_colunas} colunas
📈 Volumetria:          {stats[0]:,} registros
👤 Cardinalidade:       {stats[1]:,} CPFs únicos
📌 Grão da Tabela:      CPF + SAFRA + PROD
{"="*65}
"""
    print(report_log)
    
    os.makedirs(QUALITY_REPORT_PATH.parent, exist_ok=True)
    with open(QUALITY_REPORT_PATH, "w") as f: 
        f.write(report_log)

    con.execute(f"COPY (SELECT * FROM work_db.gold_step1 ORDER BY ano_mes) TO '{GOLD_PATH}' (FORMAT PARQUET, PARTITION_BY (ano_mes), OVERWRITE_OR_IGNORE 1)")
    
    con.execute("DETACH work_db")
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)
    
    cleanup_old_runs(bucket="lake", base_path=GOLD_BASE_PATH, max_runs=MAX_GOLD_RUNS, protect_run_id=RUN_ID)
    print(f"🏁 ABT persistida em: {GOLD_PATH}")

if __name__ == "__main__":
    run()