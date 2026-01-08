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
RAW_PATH = "s3://lake/raw/telco/*.parquet"

RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
BRONZE_BASE_PATH = "bronze/telco/"
BRONZE_PATH = f"s3://lake/{BRONZE_BASE_PATH}run_id={RUN_ID}/"

# Política de retenção
MAX_BRONZE_RUNS = int(os.getenv("BRONZE_MAX_RUNS", 1))

def run():
    con = get_duckdb_connection(
        memory_limit="6GB",
        threads=5,
    )

    print("🚀 Iniciando Bronze: telco")
    print(f"🧾 run_id = {RUN_ID}")
    print(f"🧹 Política de retenção: manter {MAX_BRONZE_RUNS} runs")

    # ------------------------------------------------------------------
    # Transformação RAW -> BRONZE
    # ------------------------------------------------------------------
    query = f"""
            CREATE OR REPLACE TABLE bronze_telco AS
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
                    -- Domínios e Atributos (VARCHAR)
                    -- ----------------------------
                    PROD::VARCHAR AS prod,
                    flag_mig2::VARCHAR AS flag_mig2,
                    var_26::VARCHAR AS var_26,
                    var_27::VARCHAR AS var_27,
                    var_64::VARCHAR AS var_64,
                    var_65::VARCHAR AS var_65,
                    var_66::VARCHAR AS var_66,
                    var_67::VARCHAR AS var_67,
                    var_73::VARCHAR AS var_73,
                    var_74::VARCHAR AS var_74,
                    var_75::VARCHAR AS var_75,
                    var_76::VARCHAR AS var_76,
                    var_77::VARCHAR AS var_77,
                    var_78::VARCHAR AS var_78,
                    var_79::VARCHAR AS var_79,
                    var_80::VARCHAR AS var_80,
                    var_81::VARCHAR AS var_81,
                    var_83::VARCHAR AS var_83,
                    var_84::VARCHAR AS var_84,
                    var_85::VARCHAR AS var_85,
                    var_86::VARCHAR AS var_86,
                    var_87::VARCHAR AS var_87,
                    var_88::VARCHAR AS var_88,
                    var_89::VARCHAR AS var_89,
                    var_91::VARCHAR AS var_91,
                    var_92::VARCHAR AS var_92,
                    var_93::VARCHAR AS var_93,

                    -- ----------------------------
                    -- Variáveis Numéricas (DOUBLE)
                    -- ----------------------------
                    var_28::DOUBLE AS var_28,
                    var_29::DOUBLE AS var_29,
                    var_30::DOUBLE AS var_30,
                    var_31::DOUBLE AS var_31,
                    var_32::DOUBLE AS var_32,
                    var_33::DOUBLE AS var_33,
                    var_34::DOUBLE AS var_34,
                    var_35::DOUBLE AS var_35,
                    var_36::DOUBLE AS var_36,
                    var_37::DOUBLE AS var_37,
                    var_38::DOUBLE AS var_38,
                    var_39::DOUBLE AS var_39,
                    var_40::DOUBLE AS var_40,
                    var_41::DOUBLE AS var_41,
                    var_42::DOUBLE AS var_42,
                    var_43::DOUBLE AS var_43,
                    var_44::DOUBLE AS var_44,
                    var_45::DOUBLE AS var_45,
                    var_46::DOUBLE AS var_46,
                    var_47::DOUBLE AS var_47,
                    var_48::DOUBLE AS var_48,
                    var_49::DOUBLE AS var_49,
                    var_50::DOUBLE AS var_50,
                    var_51::DOUBLE AS var_51,
                    var_52::DOUBLE AS var_52,
                    var_53::DOUBLE AS var_53,
                    var_54::DOUBLE AS var_54,
                    var_55::DOUBLE AS var_55,
                    var_56::DOUBLE AS var_56,
                    var_57::DOUBLE AS var_57,
                    var_58::DOUBLE AS var_58,
                    var_59::DOUBLE AS var_59,
                    var_60::DOUBLE AS var_60,
                    var_61::DOUBLE AS var_61,
                    var_62::DOUBLE AS var_62,
                    var_63::DOUBLE AS var_63,
                    var_68::DOUBLE AS var_68,
                    var_69::DOUBLE AS var_69,
                    var_70::DOUBLE AS var_70,
                    var_71::DOUBLE AS var_71,
                    var_72::DOUBLE AS var_72,
                    var_82::DOUBLE AS var_82,
                    var_90::DOUBLE AS var_90,

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
        "SELECT COUNT(*) FROM bronze_telco"
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
            FROM bronze_telco
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

    print("🏁 Pipeline telco Bronze finalizado!")


if __name__ == "__main__":
    run()