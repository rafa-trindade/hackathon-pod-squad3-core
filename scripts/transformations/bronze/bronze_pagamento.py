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
RAW_PATH = "s3://lake/raw/pagamento/*.parquet"

RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d")
BRONZE_BASE_PATH = "bronze/pagamento/"
BRONZE_PATH = f"s3://lake/{BRONZE_BASE_PATH}run_id={RUN_ID}/"

# Política de retenção
MAX_BRONZE_RUNS = int(os.getenv("BRONZE_MAX_RUNS", 1))

def run():
    con = get_duckdb_connection()

    print("🚀 Iniciando Bronze: pagamento")
    print(f"🧾 run_id = {RUN_ID}")
    print(f"🧹 Política de retenção: manter {MAX_BRONZE_RUNS} runs")

    # ------------------------------------------------------------------
    # Transformação RAW -> BRONZE
    # ------------------------------------------------------------------
    query = f"""
        CREATE OR REPLACE TABLE bronze_pagamento AS
        WITH typed_data AS (
            SELECT
                -- ----------------------------
                -- Identificadores e Chaves
                -- ----------------------------
                NUM_CPF::VARCHAR AS num_cpf,
                strptime(DAT_STATUS_FATURA, '%d%b%Y:%H:%M:%S')::DATE AS dat_status_fatura,
                CONTRATO::VARCHAR AS contrato,
                DW_NUM_CLIENTE::VARCHAR AS dw_num_cliente,

                -- ----------------------------
                -- Datas (Conversão String SAS -> DATE/TIMESTAMP)
                -- ----------------------------
                strptime(DAT_CRIACAO_DW, '%d%b%Y:%H:%M:%S')::TIMESTAMP AS dat_criacao_dw,
                strptime(DAT_CRIACAO_ATIVIDADE, '%d%b%Y:%H:%M:%S')::TIMESTAMP AS dat_criacao_atividade,
                strptime(DAT_ATUALIZACAO_ATIVIDADE, '%d%b%Y:%H:%M:%S')::TIMESTAMP AS dat_atualizacao_atividade,
                strptime(DAT_BAIXA_ATIVIDADE, '%d%b%Y:%H:%M:%S')::DATE AS dat_baixa_atividade,
                strptime(DAT_DEPOSITO_ATIVIDADE, '%d%b%Y:%H:%M:%S')::DATE AS dat_deposito_atividade,
                strptime(DAT_CRIACAO_PAGAMENTO, '%d%b%Y:%H:%M:%S')::TIMESTAMP AS dat_criacao_pagamento,
                strptime(DAT_ATUALIZACAO_PAGAMENTO, '%d%b%Y:%H:%M:%S')::TIMESTAMP AS dat_atualizacao_pagamento,
                strptime(DAT_STATUS_PAGAMENTO, '%d%b%Y:%H:%M:%S')::DATE AS dat_status_pagamento,
                strptime(DAT_CRIACAO_CREDITO, '%d%b%Y:%H:%M:%S')::TIMESTAMP AS dat_criacao_credito,
                strptime(DAT_ATUALIZACAO_CREDITO, '%d%b%Y:%H:%M:%S')::TIMESTAMP AS dat_atualizacao_credito,
                strptime(DAT_ATIVIDADE_CREDITO, '%d%b%Y:%H:%M:%S')::DATE AS dat_atividade_credito,
                strptime(DAT_VENCIMENTO_CREDITO, '%d%b%Y:%H:%M:%S')::DATE AS dat_vencimento_credito,

                -- ----------------------------
                -- Valores Financeiros (DOUBLE)
                -- ----------------------------
                CAST(VAL_PAGAMENTO_FATURA AS DOUBLE) AS val_pagamento_fatura,
                CAST(VAL_DESCONTO_ITEM AS DOUBLE) AS val_desconto_item,
                CAST(VAL_PAGAMENTO_ITEM AS DOUBLE) AS val_pagamento_item,
                CAST(VAL_JUROS_MULTAS_ITEM AS DOUBLE) AS val_juros_multas_item,
                CAST(VAL_MULTA_EQUIP_ITEM AS DOUBLE) AS val_multa_equip_item,
                CAST(VAL_MULTA_EQUIP_TOTAL AS DOUBLE) AS val_multa_equip_total,
                CAST(VAL_MULTA_FID_ITEM AS DOUBLE) AS val_multa_fid_item,
                CAST(VAL_BAIXA_ATIVIDADE AS DOUBLE) AS val_baixa_atividade,
                CAST(VAL_ORIGINAL_PAGAMENTO AS DOUBLE) AS val_original_pagamento,
                CAST(VAL_ATUAL_PAGAMENTO AS DOUBLE) AS val_atual_pagamento,
                CAST(VAL_PAGAMENTO_CREDITO AS DOUBLE) AS val_pagamento_credito,

                -- ----------------------------
                -- Atributos e Categorias (VARCHAR)
                -- ----------------------------
                SEQ_FATURA::VARCHAR AS seq_fatura, 
                NUM_SUB_SEQ_FATURA::VARCHAR AS num_sub_seq_fatura, 
                NUM_CREDITO_SEQ::VARCHAR AS num_credito_seq, 
                NUM_FATURA_PAGAMENTO::VARCHAR AS num_fatura_pagamento,
                DW_TIPO_FATURA::VARCHAR AS dw_tipo_fatura, 
                IND_STATUS_FATURA::VARCHAR AS ind_status_fatura,
                DW_AREA::VARCHAR AS dw_area, 
                DW_UN_NEGOCIO::VARCHAR AS dw_un_negocio, 
                DW_FORMA_PAGAMENTO::VARCHAR AS dw_forma_pagamento, 
                DW_BANCO::VARCHAR AS dw_banco, 
                DW_TIPO_PAGAMENTO::VARCHAR AS dw_tipo_pagamento,
                NUM_BANCO_PAGAMENTO::VARCHAR AS num_banco_pagamento, 
                NUM_AGENCIA_PAGAMENTO::VARCHAR AS num_agencia_pagamento, 
                NUM_CC_PAGAMENTO::VARCHAR AS num_cc_pagamento, 
                DW_MOTIVO_ESTORNO::VARCHAR AS dw_motivo_estorno,
                COD_ORIGEM_NETUNO::VARCHAR AS cod_origem_netuno, 
                COD_CONTA_ATIVIDADE::VARCHAR AS cod_conta_atividade, 
                SEQ_ENTIDADE_ATIVIDADE::VARCHAR AS seq_entidade_atividade,
                COD_LOGIN_OPERADOR_ATIVIDADE::VARCHAR AS cod_login_operador_atividade, 
                COD_ATIVIDADE::VARCHAR AS cod_atividade, 
                COD_RAZAO_ATIVIDADE::VARCHAR AS cod_razao_atividade,
                COD_FUNDO_ATIVIDADE::VARCHAR AS cod_fundo_atividade, 
                COD_BANCO_ATIVIDADE::VARCHAR AS cod_banco_atividade, 
                NUM_CONTA_ATIVIDADE::VARCHAR AS num_conta_atividade,
                COD_AGENCIA_ATIVIDADE::VARCHAR AS cod_agencia_atividade, 
                SEQ_ENTIDADE_PAGAMENTO::VARCHAR AS seq_entidade_pagamento, 
                COD_LOGIN_PAGAMENTO::VARCHAR AS cod_login_pagamento,
                COD_FORMA_PAGAMENTO::VARCHAR AS cod_forma_pagamento, 
                COD_TIPO_PAGAMENTO::VARCHAR AS cod_tipo_pagamento, 
                DSC_NOME_BANCO_PAGAMENTO::VARCHAR AS dsc_nome_banco_pagamento,
                SEQ_ARQUIVO_PAGAMENTO::VARCHAR AS seq_arquivo_pagamento, 
                NUM_PARCELA_PAGAMENTO::VARCHAR AS num_parcela_pagamento, 
                NUM_AGRUPADOR_PAGAMENTO::VARCHAR AS num_agrupador_pagamento,
                DSC_PAGAMENTO::VARCHAR AS dsc_pagamento, 
                COD_METODO_PAGAMENTO::VARCHAR AS cod_metodo_pagamento, 
                IND_STATUS_PAGAMENTO::VARCHAR AS ind_status_pagamento,
                COD_ARQUIVO_PAGAMENTO::VARCHAR AS cod_arquivo_pagamento, 
                COD_NETUNO_PAGAMENTO::VARCHAR AS cod_netuno_pagamento, 
                COD_LOGIN_CREDITO::VARCHAR AS cod_login_credito,
                IND_TIPO_CREDITO::VARCHAR AS ind_tipo_credito, 
                SEQ_PAGAMENTO_CREDITO::VARCHAR AS seq_pagamento_credito, 
                SEQ_FATURA_CREDITO::VARCHAR AS seq_fatura_credito,
                COD_ALOCACAO_CREDITO::VARCHAR AS cod_alocacao_credito, 
                COD_DESALOCACAO_CREDITO::VARCHAR AS cod_desalocacao_credito, 
                SEQ_ENTIDADE_CREDITO::VARCHAR AS seq_entidade_credito,
                COD_TIPO_FATURA::VARCHAR AS cod_tipo_fatura
            FROM read_parquet('{RAW_PATH}')
            WHERE DAT_STATUS_FATURA IS NOT NULL
        ),
        partitioned_data AS (
            SELECT 
                *,
                ((YEAR(dat_status_fatura) * 100) + MONTH(dat_status_fatura))::BIGINT AS _ano_mes_folder,
                CURRENT_TIMESTAMP AS ingestion_ts
            FROM typed_data
        )
        SELECT * FROM partitioned_data
    """

    print("🧱 Executando transformação Bronze...")
    con.execute(query)

    rows = con.execute("SELECT COUNT(*) FROM bronze_pagamento").fetchone()[0]
    
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
                * EXCLUDE (_ano_mes_folder),
                _ano_mes_folder AS ano_mes
            FROM bronze_pagamento
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

    print("🏁 Pipeline pagamento Bronze finalizado!")
    

if __name__ == "__main__":
    run()