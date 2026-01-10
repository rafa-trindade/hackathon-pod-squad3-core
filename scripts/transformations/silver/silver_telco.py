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
TABLE_NAME = "telco"

BRONZE_PATH = f"s3://lake/bronze/{TABLE_NAME}/**/*.parquet"
RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
SILVER_BASE_PATH = f"silver/{TABLE_NAME}/"
SILVER_PATH = f"s3://lake/{SILVER_BASE_PATH}run_id={RUN_ID}/"

MAX_SILVER_RUNS = int(os.getenv("SILVER_MAX_RUNS", 1))

# ------------------------------------------------------------------
# CONFIGURAÇÃO DE SANEAMENTO
# ------------------------------------------------------------------
keys_to_clean = {
    'num_cpf': {
        'replace': [], 
        'default': '0'
    },
    
    'safra': {
        'replace': [], 
        'default': '1900-01-01'
    },

    'prod': {
        'replace': [], 
        'default': '0'
    },

        'flag_instalacao': {
        'replace': [], 
        'default': 'false'
    }

}

def run():
    con = get_duckdb_connection(
        memory_limit="6GB", 
        threads=5
    )

    con.execute("SET preserve_insertion_order = false")
    WORK_DB_PATH = f"/mnt/nvme/duckdb_temp/work_{TABLE_NAME}.db"
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)
    con.execute(f"ATTACH '{WORK_DB_PATH}' AS work_db")

    print("--------------------------------------------------")
    print(f"🚀 Iniciando Silver: {TABLE_NAME}")
    print(f"🧾 run_id = {RUN_ID}")
    
    initial_count = con.execute(f"SELECT COUNT(*) FROM read_parquet('{BRONZE_PATH}')").fetchone()[0]
    print(f"📥 Registros carregados da Bronze: {initial_count:,}".replace(",", "."))

    # ------------------------------------------------------------------
    # ETAPA 1: Normalização de Chaves (Saneamento Prévio)
    # ------------------------------------------------------------------
    print("--------------------------------------------------")
    print("🔑 Etapa 1: Saneando identificadores e colunas do grão...")
    
    if keys_to_clean:
        sql_transform = []
        diff_conditions = []

        for col, config in keys_to_clean.items():
            val_default = config['default']

            blacklist = config['replace'] + ['', 'nan', 'NULL']
            formatted_blacklist = ", ".join([f"'{x}'" for x in blacklist])

            transform_expr = f"""
                CASE 
                    WHEN TRIM({col}::VARCHAR) IN ({formatted_blacklist}) OR {col} IS NULL 
                    THEN '{val_default}' 
                    ELSE TRIM({col}::VARCHAR) 
                END
            """
            sql_transform.append(f"{transform_expr} AS {col}")

            diff_conditions.append(f"SUM(CASE WHEN {col}::VARCHAR IS DISTINCT FROM ({transform_expr}) THEN 1 ELSE 0 END) AS diff_{col}")


        stats_query = f"SELECT {', '.join(diff_conditions)} FROM read_parquet('{BRONZE_PATH}')"
        stats_result = con.execute(stats_query).fetchone()

        con.execute(f"""
            CREATE TABLE work_db.silver_{TABLE_NAME}_step1 AS
            SELECT 
                * EXCLUDE({', '.join(keys_to_clean.keys())}),
                {', '.join(sql_transform)}
            FROM read_parquet('{BRONZE_PATH}')
        """)
        con.execute("CHECKPOINT work_db")

        for i, col in enumerate(keys_to_clean.keys()):
            diff_count = stats_result[i]
            if diff_count > 0:
                print(f"✨ Coluna '{col}': {diff_count:,} registros normalizados para '{keys_to_clean[col]['default']}'.".replace(",", "."))
            else:
                print(f"✨ Coluna '{col}': Já estava em conformidade.")

    # ------------------------------------------------------------------
    # ETAPA 2: Deduplicação
    # ------------------------------------------------------------------
    print("--------------------------------------------------")
    print("💎 Etapa 2: Validando necessidade de deduplicação...")
    
    step1_table = f"work_db.silver_{TABLE_NAME}_step1"
    chave_tecnica_cols = list(keys_to_clean.keys())
    chave_cols_str = ", ".join(chave_tecnica_cols)

    check_duplicados = con.execute(f"""
        SELECT 
            COUNT(*) as total,
            COUNT(DISTINCT ({chave_cols_str})) as distintos
        FROM {step1_table}
    """).fetchone()

    total_linhas = check_duplicados[0]
    total_distintos = check_duplicados[1]
    qtd_duplicados = total_linhas - total_distintos

    if qtd_duplicados > 0:
        print(f"⚠️ Detectados {qtd_duplicados:,} registros duplicados. Iniciando deduplicação...".replace(",", "."))
        
        con.execute(f"""
            CREATE TABLE work_db.chaves_duplicadas AS 
            SELECT {chave_cols_str} FROM {step1_table} 
            GROUP BY {chave_cols_str} HAVING COUNT(*) > 1
        """)

        con.execute(f"""
            CREATE TABLE work_db.silver_{TABLE_NAME}_step2 AS
            SELECT * FROM {step1_table} t
            WHERE NOT EXISTS (
                SELECT 1 FROM work_db.chaves_duplicadas d 
                WHERE {' AND '.join([f't.{c} = d.{c}' for c in chave_tecnica_cols])}
            )
            UNION ALL
            SELECT * EXCLUDE(row_num) FROM (
                SELECT t.*, 
                       ROW_NUMBER() OVER(PARTITION BY {", ".join([f"t.{c}" for c in chave_tecnica_cols])} ORDER BY ingestion_ts DESC) as row_num
                FROM {step1_table} t
                JOIN work_db.chaves_duplicadas d ON {' AND '.join([f't.{c} = d.{c}' for c in chave_tecnica_cols])}
            ) WHERE row_num = 1
        """)
        con.execute("CHECKPOINT work_db")
        
        step2_table = f"work_db.silver_{TABLE_NAME}_step2"
        final_count = con.execute(f"SELECT COUNT(*) FROM {step2_table}").fetchone()[0]
        print(f"✨ Unicidade garantida: {final_count:,} registros mantidos.".replace(",", "."))
    else:
        print("✅ Nenhuma duplicata detectada. Ignorando etapa de deduplicação.")
        con.execute(f"CREATE VIEW work_db.silver_{TABLE_NAME}_step2 AS SELECT * FROM {step1_table}")
        final_count = total_linhas

    # ------------------------------------------------------------------
    # ETAPA 3: Limpeza de Colunas
    # ------------------------------------------------------------------
    print("--------------------------------------------------")
    print("🧹 Etapa 3: Analisando colunas e reordenando schema...")
    
    step2_table = f"work_db.silver_{TABLE_NAME}_step2"
    
    all_columns = con.execute(f"DESCRIBE {step2_table}").df()['column_name'].tolist()
    
    null_counts = con.execute(f"SELECT {', '.join([f'COUNT({c}) AS {c}' for c in all_columns])} FROM {step2_table}").df()
    cols_to_drop = [col for col in null_counts.columns if null_counts[col][0] == 0]
    
    cols_remaining = [c for c in all_columns if c not in cols_to_drop]
    
    metadata_cols = ['ingestion_ts', 'run_id', 'ano_mes']
    business_keys = list(keys_to_clean.keys())
    
    other_cols = sorted([c for c in cols_remaining if c not in business_keys and c not in metadata_cols])
    
    ordered_cols = business_keys + other_cols + [c for c in metadata_cols if c in cols_remaining]

    final_table = f"work_db.silver_{TABLE_NAME}_final"
    con.execute(f"CREATE TABLE {final_table} AS SELECT {', '.join(ordered_cols)} FROM {step2_table}")

    if cols_to_drop:
        print(f"✂️ Colunas 100% nulas excluídas: {cols_to_drop}")
    else:
        print("✨ Nenhuma coluna 100% nula encontrada.")
    print(f"🔄 Schema reordenado: {len(ordered_cols)} colunas processadas.")

    # ------------------------------------------------------------------
    # Gravação Parquet (S3)
    # ------------------------------------------------------------------
    print("--------------------------------------------------")
    print(f"💾 Gravando dados na camada Silver (Run: {RUN_ID})...")
    con.execute(f"COPY (SELECT * FROM {final_table} ORDER BY ano_mes) TO '{SILVER_PATH}' (FORMAT PARQUET, PARTITION_BY (ano_mes), OVERWRITE_OR_IGNORE 1)")
    
    # ------------------------------------------------------------------
    # Limpeza Final
    # ------------------------------------------------------------------
    con.execute("DETACH work_db")
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)

    print("--------------------------------------------------")
    print("🧹 Aplicando política de retenção na Silver...")
    cleanup_old_runs(bucket="lake", base_path=SILVER_BASE_PATH, max_runs=MAX_SILVER_RUNS, protect_run_id=RUN_ID)

    print("--------------------------------------------------")
    print(f"🏁 Pipeline {TABLE_NAME} Silver finalizado! Registros: {final_count:,}".replace(",", "."))

if __name__ == "__main__":
    run()