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
RAW_PATH = "s3://lake/raw/atraso/*.parquet"

RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
BRONZE_BASE_PATH = "bronze/atraso/"
BRONZE_PATH = f"s3://lake/{BRONZE_BASE_PATH}run_id={RUN_ID}/"

# Política de retenção
MAX_BRONZE_RUNS = int(os.getenv("BRONZE_MAX_RUNS", 1))

def run():
    con = get_duckdb_connection()

    print(f"🚀 Iniciando Bronze: atraso")
    print(f"🧾 run_id = {RUN_ID}")
    print(f"🧹 Política de retenção: manter {MAX_BRONZE_RUNS} runs")

    # ------------------------------------------------------------------
    # Transformação RAW -> BRONZE
    # ------------------------------------------------------------------
    query = f"""
        CREATE OR REPLACE TABLE bronze_atraso AS
        WITH typed_data AS (
            SELECT
                -- ----------------------------
                -- Identificadores e Tempo
                -- ----------------------------
                NUM_CPF::VARCHAR AS num_cpf,
                strptime(DAT_REFERENCIA, '%d%b%Y:%H:%M:%S')::DATE AS dat_referencia,
                NUM_FATURA_HASH::VARCHAR AS num_fatura_hash,
                CONTRATO::VARCHAR AS contrato,
                DW_NUM_CLIENTE::VARCHAR AS dw_num_cliente,
                
                -- ----------------------------
                -- Datas (Conversão String -> DATE/TIMESTAMP)
                -- ----------------------------
                strptime(DAT_CRIACAO_REGISTRO_TRANS, '%d%b%Y:%H:%M:%S')::TIMESTAMP AS dat_criacao_registro_trans,
                strptime(DAT_ALTERACAO_REGISTRO_TRANS, '%d%b%Y:%H:%M:%S')::TIMESTAMP AS dat_alteracao_registro_trans,
                strptime(DAT_CANCELAMENTO_FAT, '%d%b%Y:%H:%M:%S')::DATE AS dat_cancelamento_fat,
                strptime(DAT_ORIGINAL_VCTO_FAT, '%d%b%Y:%H:%M:%S')::DATE AS dat_original_vcto_fat,
                strptime(DAT_ALTERACAO_VCTO_FAT, '%d%b%Y:%H:%M:%S')::DATE AS dat_alteracao_vcto_fat,
                strptime(DAT_CRIACAO_FAT, '%d%b%Y:%H:%M:%S')::TIMESTAMP AS dat_criacao_fat,
                strptime(DAT_VENCIMENTO_FAT, '%d%b%Y:%H:%M:%S')::DATE AS dat_vencimento_fat,
                strptime(DAT_STATUS_FAT, '%d%b%Y:%H:%M:%S')::TIMESTAMP AS dat_status_fat,
                strptime(DAT_MIN_VENCIMENTO_FAT, '%d%b%Y:%H:%M:%S')::DATE AS dat_min_vencimento_fat,
                strptime(DAT_ATIVACAO_CONTA_CLI, '%d%b%Y:%H:%M:%S')::DATE AS dat_ativacao_conta_cli,
                strptime(DAT_CRIACAO_DW, '%d%b%Y:%H:%M:%S')::TIMESTAMP AS dat_criacao_dw,

                -- ----------------------------
                -- Domínios e Atributos (VARCHAR)
                -- ----------------------------
                NUM_ENT_SEQ_FATURA::VARCHAR AS num_ent_seq_fatura,
                DW_UN_NEGOCIO::VARCHAR AS dw_un_negocio,
                DW_HIS_PONTO_VENDA_COMTA::VARCHAR AS dw_his_ponto_venda_comta,
                DW_AREA::VARCHAR AS dw_area,
                DW_CICLO::VARCHAR AS dw_ciclo,
                DW_TIPO_CLIENTE_CONTA::VARCHAR AS dw_tipo_cliente_conta,
                DW_OFERTA::VARCHAR AS dw_oferta,
                DW_FAIXA_AGING_FATURA::VARCHAR AS dw_faixa_aging_fatura,
                DW_FAIXA_AGING_DIVIDA::VARCHAR AS dw_faixa_aging_divida,
                DW_FAIXA_TEMPO_BASE::VARCHAR AS dw_faixa_tempo_base,
                DW_FAIXA_AGING_PROX_FECH::VARCHAR AS dw_faixa_aging_prox_fech,
                DW_TIPO_FATURAMENTO::VARCHAR AS dw_tipo_faturamento,
                COD_PLATAFORMA::VARCHAR AS cod_plataforma,
                NUM_BILL_SEQ_FAT::VARCHAR AS num_bill_seq_fat,
                NUM_SEQ_ACORDO_FAT::VARCHAR AS num_seq_acordo_fat,
                IND_ISENCAO_COB_FAT::VARCHAR AS ind_isencao_cob_fat,
                IND_WO::VARCHAR AS ind_wo,
                IND_PDD::VARCHAR AS ind_pdd,
                IND_PCCR::VARCHAR AS ind_pccr,
                IND_ACA::VARCHAR AS ind_aca,
                IND_PRIMEIRA_FAT::VARCHAR AS ind_primeira_fat,
                IND_FRAUDE::VARCHAR AS ind_fraude,

                -- ----------------------------
                -- Valores e Variáveis (Numéricos)
                -- ----------------------------
                VAL_FAT_LIQUIDO::DOUBLE AS val_fat_liquido,
                VAL_FAT_BRUTO::DOUBLE AS val_fat_bruto,
                VAL_FAT_CREDITO::DOUBLE AS val_fat_credito,
                VAL_FAT_AJUSTE::DOUBLE AS val_fat_ajuste,
                VAL_FAT_BRUTO_BC::DOUBLE AS val_fat_bruto_bc,
                VAL_FAT_PAGAMENTO_BRUTO::DOUBLE AS val_fat_pagamento_bruto,
                VAL_FAT_ABERTO::DOUBLE AS val_fat_aberto,
                VAL_FAT_ABERTO_LIQ::DOUBLE AS val_fat_aberto_liq,
                VAL_MULTA_JUROS::DOUBLE AS val_multa_juros,
                VAL_MULTA_CANCELAMENTO::DOUBLE AS val_multa_cancelamento,
                VAL_PARC_APARELHO_LIQ::DOUBLE AS val_parc_aparelho_liq,
                VAL_FAT_LIQ_JM_MC::DOUBLE AS val_fat_liq_jm_mc,

                -- Campo técnico para partição
                ((YEAR(strptime(DAT_REFERENCIA, '%d%b%Y:%H:%M:%S')) * 100) + MONTH(strptime(DAT_REFERENCIA, '%d%b%Y:%H:%M:%S')))::BIGINT AS _ano_mes_folder
                
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

    rows = con.execute(f"SELECT COUNT(*) FROM bronze_atraso").fetchone()[0]
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
            FROM bronze_atraso
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

    print("🏁 Pipeline atraso Bronze finalizado!")


if __name__ == "__main__":
    run()