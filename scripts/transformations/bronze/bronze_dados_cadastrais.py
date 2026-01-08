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
RAW_PATH = f"s3://lake/raw/dados_cadastrais/*.parquet"

RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
BRONZE_BASE_PATH = f"bronze/dados_cadastrais/"
BRONZE_PATH = f"s3://lake/{BRONZE_BASE_PATH}run_id={RUN_ID}/"

# Política de retenção
MAX_BRONZE_RUNS = int(os.getenv("BRONZE_MAX_RUNS", 1))

def run():
    con = get_duckdb_connection(
        memory_limit="6GB",
        threads=5,
    )

    print(f"🚀 Iniciando Bronze: dados_cadastrais")
    print(f"🧾 run_id = {RUN_ID}")
    print(f"🧹 Política de retenção: manter {MAX_BRONZE_RUNS} runs")

    # ------------------------------------------------------------------
    # Transformação RAW -> BRONZE
    # ------------------------------------------------------------------
    query = f"""
        CREATE OR REPLACE TABLE bronze_dados_cadastrais AS
        WITH typed_data AS (
            SELECT
                -- ----------------------------
                -- Identificadores e Tempo
                -- ----------------------------
                NUM_CPF::VARCHAR AS num_cpf,
                MAKE_DATE(
                    CAST(CAST(SAFRA AS INTEGER) / 100 AS INTEGER),
                    CAST(CAST(SAFRA AS INTEGER) % 100 AS INTEGER),
                    1
                ) AS safra,
                
                -- ----------------------------
                -- Datas (Conversão String -> DATE)
                -- ----------------------------
                TRY_CAST(strptime(DATADENASCIMENTO, '%d/%m/%Y') AS DATE) AS datadenascimento,
                TRY_CAST(strptime(var_12, '%d/%m/%Y') AS DATE) AS var_12,

                -- Tratamento especial var_13 (Mistos DD/MM/YYYY e DDMM)
                CASE 
                    WHEN var_13 LIKE '%/%/%' 
                        THEN TRY_CAST(strptime(var_13, '%d/%m/%Y') AS DATE)
                    WHEN LENGTH(var_13) = 4 
                        THEN MAKE_DATE(
                            CAST(CAST(SAFRA AS INTEGER) / 100 AS INTEGER),
                            CAST(RIGHT(var_13, 2) AS INTEGER),
                            1
                        )
                    ELSE NULL 
                END AS var_13,

                -- ----------------------------
                -- Flags (Booleans)
                -- ----------------------------
                CAST(FLAG_INSTALACAO = '1' AS BOOLEAN) AS flag_instalacao,
                CAST(FPD = '1' AS BOOLEAN) AS fpd,

                -- ----------------------------
                -- Domínios e Atributos (VARCHAR)
                -- ----------------------------
                PROD::VARCHAR AS prod,
                flag_mig2::VARCHAR AS flag_mig2,
                STATUSRF::VARCHAR AS statusrf,
                var_10::VARCHAR AS var_10,
                var_15::VARCHAR AS var_15,
                var_18::VARCHAR AS var_18,
                var_19::VARCHAR AS var_19,
                var_20::VARCHAR AS var_20,
                var_21::VARCHAR AS var_21,
                var_22::VARCHAR AS var_22,
                var_23::VARCHAR AS var_23,
                var_24::VARCHAR AS var_24,
                var_25::VARCHAR AS var_25,
                CEP_3_digitos::VARCHAR AS cep_3_digitos,

                -- ----------------------------
                -- Valores e Variáveis (Numéricos)
                -- ----------------------------
                var_03::INTEGER AS var_03,
                var_02::INTEGER AS var_02,
                var_04::INTEGER AS var_04,
                var_05::INTEGER AS var_05,
                var_06::INTEGER AS var_06,
                var_07::DOUBLE AS var_07,
                var_08::INTEGER AS var_08,
                var_09::INTEGER AS var_09,
                var_11::DOUBLE AS var_11,
                var_14::INTEGER AS var_14,
                var_16::INTEGER AS var_16,
                var_17::INTEGER AS var_17,

                -- Campo técnico para partição
                CAST(SAFRA AS BIGINT) AS _ano_mes_folder
                
            FROM read_parquet('{RAW_PATH}')
        ),
        partitioned_data AS (
            SELECT 
                *,
                CURRENT_TIMESTAMP AS ingestion_ts
            FROM typed_data
        )
        SELECT * FROM partitioned_data
    """

    print("🧱 Executando transformação Bronze...")
    con.execute(query)

    rows = con.execute(f"SELECT COUNT(*) FROM bronze_dados_cadastrais").fetchone()[0]
    print(f"📊 Total de linhas na Bronze: {rows:,}".replace(",", "."))

    if rows == 0:
        raise RuntimeError("❌ Erro: A transformação gerou 0 linhas.")

    # ------------------------------------------------------------------
    # Escrita em Parquet (Particionado por ano_mes)
    # ------------------------------------------------------------------
    print("💾 Gravando dados na camada Bronze (Partição ano_mes)...")
    con.execute(f"""
        COPY (
            SELECT 
                * EXCLUDE (_ano_mes_folder),
                _ano_mes_folder AS ano_mes
            FROM bronze_dados_cadastrais
            ORDER BY ano_mes, num_cpf
        )
        TO '{BRONZE_PATH}'
        (
            FORMAT PARQUET,
            PARTITION_BY (ano_mes),
            OVERWRITE_OR_IGNORE 1
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

    print("🏁 Pipeline dados_cadastrais Bronze finalizado!")


if __name__ == "__main__":
    run()