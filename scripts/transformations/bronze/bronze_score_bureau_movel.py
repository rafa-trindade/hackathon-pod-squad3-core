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
RAW_PATH = "s3://lake/raw/score_bureau_movel/*.parquet"

RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
BRONZE_BASE_PATH = "bronze/score_bureau_movel/"
BRONZE_PATH = f"s3://lake/{BRONZE_BASE_PATH}run_id={RUN_ID}/"

# Política de retenção
MAX_BRONZE_RUNS = int(os.getenv("BRONZE_MAX_RUNS", 1))

def run():
    con = get_duckdb_connection(
        memory_limit="6GB",
        threads=5,
    )

    print("🚀 Iniciando Bronze: score_bureau_movel")
    print(f"🧾 run_id = {RUN_ID}")
    print(f"🧹 Política de retenção: manter {MAX_BRONZE_RUNS} runs")

    # ------------------------------------------------------------------
    # Transformação RAW -> BRONZE
    # ------------------------------------------------------------------
    query = f"""
            CREATE OR REPLACE TABLE bronze_score_bureau_movel AS
            WITH typed_data AS (
                SELECT
                    -- ----------------------------
                    -- Tempo e Identificadores
                    -- ----------------------------
                    NUM_CPF::VARCHAR AS num_cpf,
                    MAKE_DATE(
                        CAST(CAST(SAFRA AS INTEGER) / 100 AS INTEGER),
                        CAST(CAST(SAFRA AS INTEGER) % 100 AS INTEGER),
                        1
                    ) AS safra,


                    -- ----------------------------
                    -- Flags (Booleans)
                    -- ----------------------------
                    CAST(FLAG_INSTALACAO = '1' AS BOOLEAN) AS flag_instalacao,
                    CAST(FPD = '1' AS BOOLEAN) AS fpd,

                    -- ----------------------------
                    -- Domínios (Categorias)
                    -- ----------------------------
                    PROD::VARCHAR AS prod,
                    flag_mig2::VARCHAR AS flag_mig2,

                    -- ----------------------------
                    -- Scores (Integers)
                    -- ----------------------------
                    CAST(SCORE_01 AS INTEGER) AS score_01,
                    CAST(SCORE_02 AS INTEGER) AS score_02,

                    -- Campo técnico para partição
                    CAST(SAFRA AS BIGINT) AS ano_mes_folder,
                    
                    CURRENT_TIMESTAMP AS ingestion_ts
                    
                FROM read_parquet('{RAW_PATH}')
            )
            SELECT * FROM typed_data
        """

    print("🧱 Executando transformação Bronze...")
    con.execute(query)

    rows = con.execute(
        "SELECT COUNT(*) FROM bronze_score_bureau_movel"
    ).fetchone()[0]

    print(f"📊 Total de linhas na Bronze: {rows:,}".replace(",", "."))

    if rows == 0:
        raise RuntimeError("❌ Bronze gerou 0 linhas - abortando escrita")

    # ------------------------------------------------------------------
    # Escrita em Parquet (Particionamento por ano_mes)
    # ------------------------------------------------------------------
    print("💾 Gravando dados na camada Bronze (Partição ano_mes)...")
    con.execute(f"""
        COPY (
            SELECT 
                * EXCLUDE (ano_mes_folder),
                ano_mes_folder AS ano_mes
            FROM bronze_score_bureau_movel
            ORDER BY ano_mes, num_cpf
        )
        TO '{BRONZE_PATH}'
        (
            FORMAT PARQUET,
            PARTITION_BY (ano_mes)
        )
    """)

    print("✅ Carga Bronze finalizada com sucesso!")

    # ------------------------------------------------------------------
    # Limpeza de runs antigas
    # ------------------------------------------------------------------
    print("🧹 Aplicando política de retenção de runs...")
    cleanup_old_runs(
        bucket="lake",
        base_path=BRONZE_BASE_PATH,
        max_runs=MAX_BRONZE_RUNS,
        protect_run_id=RUN_ID,
    )

    print("🏁 Pipeline score_bureau_movel Bronze finalizado!")


if __name__ == "__main__":
    run()