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
MAX_BRONZE_RUNS = int(os.getenv("BRONZE_MAX_RUNS", 3))


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
        SELECT
            -- ----------------------------
            -- Tempo
            -- ----------------------------
            MAKE_DATE(
                CAST(CAST(SAFRA AS INTEGER) / 100 AS INTEGER),
                CAST(CAST(SAFRA AS INTEGER) % 100 AS INTEGER),
                1
            ) AS safra_date,

            LPAD(CAST(SAFRA AS VARCHAR), 6, '0') AS safra,

            -- ----------------------------
            -- Flags
            -- ----------------------------
            CAST(FLAG_INSTALACAO = '1' AS BOOLEAN) AS has_instalacao,
            CAST(FPD = '1' AS BOOLEAN) AS is_fpd,

            -- ----------------------------
            -- Domínios
            -- ----------------------------
            PROD AS produto,
            flag_mig2 AS tipo_migracao,

            -- ----------------------------
            -- Scores
            -- ----------------------------
            CAST(SCORE_01 AS INTEGER) AS score_principal,
            CAST(SCORE_02 AS INTEGER) AS score_secundario,

            -- ----------------------------
            -- Identificador
            -- ----------------------------
            NUM_CPF AS cpf_hash,

            -- ----------------------------
            -- Metadados técnicos
            -- ----------------------------
            CURRENT_TIMESTAMP AS ingestion_ts,
            filename AS source_file

        FROM read_parquet('{RAW_PATH}')
    """

    print("🧱 Executando transformação Bronze...")
    con.execute(query)

    rows = con.execute(
        "SELECT COUNT(*) FROM bronze_score_bureau_movel"
    ).fetchone()[0]

    print(f"📊 Total de linhas na Bronze: {rows:,}".replace(",", "."))

    if rows == 0:
        raise RuntimeError("❌ Bronze gerou 0 linhas — abortando escrita")

    # ------------------------------------------------------------------
    # Escrita em Parquet (Bronze)
    # ------------------------------------------------------------------
    print("💾 Gravando dados na camada Bronze...")
    con.execute(f"""
        COPY (
            SELECT *
            FROM bronze_score_bureau_movel
            ORDER BY safra, cpf_hash
        )
        TO '{BRONZE_PATH}'
        (
            FORMAT PARQUET,
            PARTITION_BY (safra)
        )
    """)

    print("✅ Escrita Bronze concluída com sucesso")

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

    print("🏁 Pipeline score_bureau_movel Bronze finalizado com sucesso!")


if __name__ == "__main__":
    run()
