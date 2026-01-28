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
RAW_PATH = f"s3://lake/raw/recarga/*.parquet"

RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d")
BRONZE_BASE_PATH = f"bronze/recarga/"
BRONZE_PATH = f"s3://lake/{BRONZE_BASE_PATH}run_id={RUN_ID}/"

# Política de retenção
MAX_BRONZE_RUNS = int(os.getenv("BRONZE_MAX_RUNS", 1))

def run():
    con = get_duckdb_connection()

    print(f"🚀 Iniciando Bronze: recarga")
    print(f"🧾 run_id = {RUN_ID}")
    print(f"🧹 Política de retenção: manter {MAX_BRONZE_RUNS} runs")

    # ------------------------------------------------------------------
    # Transformação RAW -> BRONZE
    # ------------------------------------------------------------------
    query = f"""
        CREATE OR REPLACE TABLE bronze_recarga AS
        WITH typed_data AS (
            SELECT
                -- ----------------------------
                -- Identificadores e Tempo
                -- ----------------------------
                NUM_CPF::VARCHAR AS num_cpf,
                strptime(DAT_INSERCAO_CREDITO, '%d%b%Y:%H:%M:%S')::DATE AS dat_insercao_credito,
                HOR_INSERCAO_CREDITO::VARCHAR AS hor_insercao_credito,
                DW_NUM_NTC::VARCHAR AS dw_num_ntc,
                DW_NUM_CLIENTE::VARCHAR AS dw_num_cliente,

                -- ----------------------------
                -- Flags (Booleans)
                -- ----------------------------
                CAST(FLAG_SOS = '1' AS BOOLEAN) AS flag_sos,

                -- ----------------------------
                -- Domínios e Atributos (VARCHAR)
                -- ----------------------------
                COD_TECNOLOGIA_DW::VARCHAR AS cod_tecnologia_dw,
                COD_CANAL_AQUISICAO::VARCHAR AS cod_canal_aquisicao,
                COD_TIPO_CREDITO::VARCHAR AS cod_tipo_credito,
                COD_PROMOCAO::VARCHAR AS cod_promocao,
                COD_PLATAFORMA_ATU::VARCHAR AS cod_plataforma_atu,
                COD_STATUS_PLATAFORMA::VARCHAR AS cod_status_plataforma,
                IND_METODO_PAGAMENTO::VARCHAR AS ind_metodo_pagamento,
                DW_PLANO_TARIFACAO::VARCHAR AS dw_plano_tarifacao,
                DW_TIPO_RECARGA::VARCHAR AS dw_tipo_recarga,
                DW_TIPO_INSERCAO::VARCHAR AS dw_tipo_insercao,
                DW_FORMA_PAGAMENTO::VARCHAR AS dw_forma_pagamento,
                DW_INSTITUICAO::VARCHAR AS dw_instituicao,
                COD_GRUPO_CARTAO::VARCHAR AS cod_grupo_cartao,
                DSC_GRUPO_CARTAO_WPP::VARCHAR AS dsc_grupo_cartao_wpp,

                -- ----------------------------
                -- Valores e Variáveis (Numéricos)
                -- ----------------------------
                VAL_CREDITO_INSERIDO::DOUBLE AS val_credito_inserido,
                VAL_BONUS::DOUBLE AS val_bonus,
                VAL_REAL::DOUBLE AS val_real,
                VALOR_SOS::DOUBLE AS valor_sos,

                -- Campo técnico para partição
                ((YEAR(strptime(DAT_INSERCAO_CREDITO, '%d%b%Y:%H:%M:%S')) * 100) + MONTH(strptime(DAT_INSERCAO_CREDITO, '%d%b%Y:%H:%M:%S')))::BIGINT AS _ano_mes_folder
                
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

    rows = con.execute(f"SELECT COUNT(*) FROM bronze_recarga").fetchone()[0]
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
            FROM bronze_recarga
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

    print("🏁 Pipeline recarga Bronze finalizado!")


if __name__ == "__main__":
    run()