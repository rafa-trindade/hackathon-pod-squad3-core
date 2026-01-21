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
TARGET_TABLE = "abt_base_prod"
ANCHOR_PATH = "s3://lake/gold/labels_fpd/**/*.parquet"

RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
GOLD_BASE_PATH = f"gold/{TARGET_TABLE}/"
GOLD_PATH = f"s3://lake/{GOLD_BASE_PATH}run_id={RUN_ID}/"

QUALITY_REPORT_PATH = PROJECT_ROOT / "reports" / "observability" / "quality" / "pipeline" / f"gold-{TARGET_TABLE}-quality.log"

MAX_GOLD_RUNS = int(os.getenv("GOLD_MAX_RUNS", 1))

def run():
    con = get_duckdb_connection(memory_limit="12GB", threads=8)
    con.execute("SET preserve_insertion_order = false")
    
    WORK_DB_PATH = f"/mnt/nvme/duckdb_temp/work_{TARGET_TABLE}.db"
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)
    con.execute(f"ATTACH '{WORK_DB_PATH}' AS work_db")

    print("--------------------------------------------------")
    print(f"🏆 Iniciando Gold ABT: {TARGET_TABLE}")
    
    # ------------------------------------------------------------------
    # ETAPA 1: AGREGAÇÕES TRANSACIONAIS
    # ------------------------------------------------------------------
    print("🎯 Etapa 1: Agregando histórico transacional...")

    con.execute("""
        CREATE TABLE work_db.agg_recarga AS
        WITH base_anchor AS (SELECT DISTINCT num_cpf, safra FROM read_parquet('s3://lake/gold/labels_fpd/**/*.parquet'))
        SELECT 
            b.num_cpf, b.safra,
            COUNT(r.val_credito_inserido) as rec_qtd_total,
            SUM(r.val_credito_inserido) as rec_vlr_total,
            AVG(r.val_credito_inserido) as rec_vlr_avg,
            MIN(r.val_credito_inserido) as rec_vlr_min,
            MAX(r.val_credito_inserido) as rec_vlr_max,
            MIN(r.dat_insercao_credito) as rec_dat_primeira,
            MAX(r.dat_insercao_credito) as rec_dat_ultima,
            COUNT(DISTINCT r.cod_canal_aquisicao) as rec_qtd_canais_distintos
        FROM base_anchor b
        LEFT JOIN read_parquet('s3://lake/silver/recarga/**/*.parquet') r 
            ON b.num_cpf = r.num_cpf AND r.dat_insercao_credito < b.safra
        GROUP BY 1, 2
    """)

    con.execute("""
        CREATE TABLE work_db.agg_pagamento AS
        WITH base_anchor AS (SELECT DISTINCT num_cpf, safra FROM read_parquet('s3://lake/gold/labels_fpd/**/*.parquet'))
        SELECT 
            b.num_cpf, b.safra,
            SUM(p.val_pagamento_fatura) as pag_vlr_total,
            AVG(p.val_pagamento_fatura) as pag_vlr_avg,
            MIN(p.val_pagamento_fatura) as pag_vlr_min,
            MAX(p.val_pagamento_fatura) as pag_vlr_max,
            COUNT(DISTINCT p.seq_fatura) as pag_qtd_faturas,
            COUNT(p.val_juros_multas_item) FILTER (WHERE p.val_juros_multas_item > 0) as pag_qtd_vezes_com_juros
        FROM base_anchor b
        LEFT JOIN read_parquet('s3://lake/silver/pagamento/**/*.parquet') p 
            ON b.num_cpf = p.num_cpf AND p.dat_status_fatura < b.safra
        GROUP BY 1, 2
    """)

    con.execute("""
        CREATE TABLE work_db.agg_atraso AS
        WITH base_anchor AS (SELECT DISTINCT num_cpf, safra FROM read_parquet('s3://lake/gold/labels_fpd/**/*.parquet'))
        SELECT 
            b.num_cpf, b.safra,
            MAX(a.val_fat_aberto) as atr_vlr_max_hist,
            SUM(a.val_fat_aberto) as atr_vlr_acumulado_hist,
            COUNT(DISTINCT a.num_fatura_hash) as atr_qtd_faturas_atrasadas,
            MAX(a.dat_referencia) as atr_dat_ultima_ref
        FROM base_anchor b
        LEFT JOIN read_parquet('s3://lake/silver/atraso/**/*.parquet') a 
            ON b.num_cpf = a.num_cpf AND a.dat_referencia < b.safra
        GROUP BY 1, 2
    """)

    # ------------------------------------------------------------------
    # ETAPA 2: MASTER JOIN COM REORDENAÇÃO DE COLUNAS
    # ------------------------------------------------------------------
    print("🔗 Etapa 2: Executando Master Join e Reordenando Colunas...")

    def get_select_prefixed(table_path, prefix, skip_cols):
        cols = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{table_path}')").df()['column_name'].tolist()
        return ", ".join([f'"{c}" AS "{prefix}_{c}"' for c in cols if c not in skip_cols])

    keys_to_skip = ['num_cpf', 'safra', 'prod', 'fpd', 'flag_instalacao', 'ano_mes', 'ingestion_ts', 'run_id']
    cad_select = get_select_prefixed('s3://lake/silver/dados_cadastrais/**/*.parquet', 'cad', keys_to_skip)
    tel_select = get_select_prefixed('s3://lake/silver/telco/**/*.parquet', 'tel', keys_to_skip)
    bur_select = get_select_prefixed('s3://lake/silver/score_bureau_movel/**/*.parquet', 'bur', keys_to_skip)

    con.execute(f"""
        CREATE TABLE work_db.gold_step1 AS
        WITH 
        cad AS (SELECT num_cpf, safra, prod, {cad_select} FROM read_parquet('s3://lake/silver/dados_cadastrais/**/*.parquet')),
        tel AS (SELECT num_cpf, safra, prod, {tel_select} FROM read_parquet('s3://lake/silver/telco/**/*.parquet')),
        bur AS (SELECT num_cpf, safra, prod, {bur_select} FROM read_parquet('s3://lake/silver/score_bureau_movel/**/*.parquet'))
        
        SELECT 
            -- 1. Colunas Grão e Target
            a.num_cpf, a.safra, a.prod, a.fpd,

            -- 2. Colunas Agregadas (Comportamento de Pagamento/Recarga na frente)
            r.* EXCLUDE (num_cpf, safra),
            p.* EXCLUDE (num_cpf, safra),
            atr.* EXCLUDE (num_cpf, safra),

            -- 3. Colunas Silver Prefixadas
            c.* EXCLUDE (num_cpf, safra, prod),
            t.* EXCLUDE (num_cpf, safra, prod),
            b.* EXCLUDE (num_cpf, safra, prod),

            -- 4. Metadados e Particionamento
            '{RUN_ID}' AS run_id,
            now() AS ingestion_ts,
            a.ano_mes
        FROM read_parquet('{ANCHOR_PATH}') a
        LEFT JOIN cad c ON a.num_cpf = c.num_cpf AND a.safra = c.safra AND a.prod = c.prod
        LEFT JOIN tel t ON a.num_cpf = t.num_cpf AND a.safra = t.safra AND a.prod = t.prod
        LEFT JOIN bur b ON a.num_cpf = b.num_cpf AND a.safra = b.safra AND a.prod = b.prod
        LEFT JOIN work_db.agg_recarga r ON a.num_cpf = r.num_cpf AND a.safra = r.safra
        LEFT JOIN work_db.agg_pagamento p ON a.num_cpf = p.num_cpf AND a.safra = p.safra
        LEFT JOIN work_db.agg_atraso atr ON a.num_cpf = atr.num_cpf AND a.safra = atr.safra
    """)

    # ------------------------------------------------------------------
    # ETAPA 3: PERSISTÊNCIA E LOG TÉCNICO
    # ------------------------------------------------------------------
    stats = con.execute("SELECT COUNT(*), COUNT(DISTINCT num_cpf) FROM work_db.gold_step1").fetchone()
    num_colunas = con.execute("SELECT COUNT(*) FROM (DESCRIBE work_db.gold_step1)").fetchone()[0]

    report_log = f"""
                    📋 RELATÓRIO TÉCNICO ABT - {TARGET_TABLE} | RUN: {RUN_ID}
                    {"="*65}
                    ✅ Status:              ABT Gerada com Sucesso
                    📈 Volumetria:          {stats[0]:,} linhas
                    👤 Cardinalidade:       {stats[1]:,} CPFs únicos
                    📊 Total de Variáveis:  {num_colunas} colunas
                    📌 Grão da Tabela:      CPF + SAFRA + PROD
                    {"="*65}
                """
    print(report_log)
    
    os.makedirs(QUALITY_REPORT_PATH.parent, exist_ok=True)
    with open(QUALITY_REPORT_PATH, "w") as f: 
        f.write(report_log)

    con.execute(f"COPY (SELECT * FROM work_db.gold_step1 ORDER BY ano_mes) TO '{GOLD_PATH}' (FORMAT PARQUET, PARTITION_BY (ano_mes))")
    
    con.execute("DETACH work_db")
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)
    
    cleanup_old_runs(bucket="lake", base_path=GOLD_BASE_PATH, max_runs=MAX_GOLD_RUNS, protect_run_id=RUN_ID)
    print(f"🏁 Processo finalizado. Dados persistidos em: {GOLD_PATH}")

if __name__ == "__main__":
    run()