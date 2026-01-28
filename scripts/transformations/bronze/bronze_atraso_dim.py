import sys
import os
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
TABLE_NAME = "atraso_dim"
DIM_NAME = "tipo_faturamento"

RAW_CSV_PATH = f"s3://lake/raw/{TABLE_NAME}/BI_DIM_TIPO_FATURAMENTO.csv"
BRONZE_ATRASO_PATTERN = "s3://lake/bronze/atraso/**/*.parquet"
BRONZE_DEST_PATH = f"s3://lake/bronze/{TABLE_NAME}/{DIM_NAME}.parquet"

QUALITY_REPORT_PATH = PROJECT_ROOT / "reports" / "observability" / "quality" / "pipeline" / f"bronze-{TABLE_NAME}-quality.log"

def run():
    con = get_duckdb_connection()

    con.execute("SET preserve_insertion_order = false")
    WORK_DB_PATH = f"/mnt/nvme/duckdb_temp/work_{DIM_NAME}.db"
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)
    con.execute(f"ATTACH '{WORK_DB_PATH}' AS work_db")

    print("--------------------------------------------------")
    print(f"🚀 Iniciando Bronze Dimensão: {DIM_NAME}")
    
    # ------------------------------------------------------------------
    # ETAPA 1: Leitura e Tipagem (Registros Originais / Colunas Minúsculas)
    # ------------------------------------------------------------------
    print("🔑 Etapa 1: Padronizando colunas e mantendo registros originais...")
    
    con.execute(f"""
        CREATE TABLE work_db.{DIM_NAME}_step1 AS
        SELECT 
            DW_TIPO_FATURAMENTO::VARCHAR as dw_tipo_faturamento,
            DSC_TIPO_FATURAMENTO::VARCHAR as dsc_tipo_faturamento,
            DSC_TIPO_FATURAMENTO_ABREV::VARCHAR as dsc_tipo_faturamento_abrev,
            COD_TIPO_FATURAMENTO::VARCHAR as cod_dsc_tipo_faturamento
        FROM read_csv_auto('{RAW_CSV_PATH}')
    """)

    # ------------------------------------------------------------------
    # ETAPA 2: Validação de Integridade
    # ------------------------------------------------------------------
    print("--------------------------------------------------")
    print("🧪 Etapa 2: Validando match de chaves com a Bronze Atraso...")

    # Verifica tipagem na tabela de fatos
    atraso_schema = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{BRONZE_ATRASO_PATTERN}')").df()
    
    if 'dw_tipo_faturamento' in atraso_schema['column_name'].values:
        target_type = atraso_schema.loc[atraso_schema['column_name'] == 'dw_tipo_faturamento', 'column_type'].values[0]
        match_type_status = "PASS" if target_type == "VARCHAR" else "FAIL"
    else:
        target_type = "NOT_FOUND"
        match_type_status = "FAIL"

    orphans_count = con.execute(f"""
        SELECT COUNT(DISTINCT f.dw_tipo_faturamento) 
        FROM read_parquet('{BRONZE_ATRASO_PATTERN}') f
        LEFT JOIN work_db.{DIM_NAME}_step1 d ON f.dw_tipo_faturamento = d.dw_tipo_faturamento
        WHERE d.dw_tipo_faturamento IS NULL AND f.dw_tipo_faturamento IS NOT NULL
    """).fetchone()[0]

    dim_count = con.execute(f"SELECT COUNT(*) FROM work_db.{DIM_NAME}_step1").fetchone()[0]

    # Gerando o Log
    now_str = datetime.now().strftime('%Y%m%d')
    log_content = f"""
📋 QUALITY REPORT - {DIM_NAME} | RUN: {now_str}
----------------------------------------------------------------------------------
TESTE                         | STATUS    | OBSERVAÇÃO
----------------------------------------------------------------------------------
Volumetria Dimensão            | INFO      | {dim_count} registros
Chave Técnica                  | INFO      | dw_tipo_faturamento
Match de Tipagem Chave Técnica | {match_type_status.ljust(9)} | Fato: {target_type} - Dim: VARCHAR
Integridade de Chave (Fato)    | {"PASS" if orphans_count == 0 else "WARN".ljust(9)}      | {orphans_count} registros órfãos
----------------------------------------------------------------------------------
Resultado Final: {"SUCCESS" if orphans_count == 0 and match_type_status == "PASS" else "CHECK_REQUIRED"}
----------------------------------------------------------------------------------
"""
    
    os.makedirs(QUALITY_REPORT_PATH.parent, exist_ok=True)
    with open(QUALITY_REPORT_PATH, "w") as f:
        f.write(log_content)
    
    print(log_content)

    # ------------------------------------------------------------------
    # ETAPA 3: Gravação Final
    # ------------------------------------------------------------------
    print("💾 Gravando Bronze Parquet...")
    
    con.execute(f"""
        COPY (SELECT * FROM work_db.{DIM_NAME}_step1) 
        TO '{BRONZE_DEST_PATH}' (FORMAT PARQUET)
    """)

    con.execute("DETACH work_db")
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)

    print(f"🏁 Processo finalizado. Dimensão salva em: {BRONZE_DEST_PATH}")

if __name__ == "__main__":
    run()