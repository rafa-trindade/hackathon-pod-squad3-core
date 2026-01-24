import pandera as pa
import duckdb
import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional
from pandera.typing import Series
import warnings


os.environ["DISABLE_PANDERA_IMPORT_WARNING"] = "True"
warnings.filterwarnings("ignore", category=FutureWarning)

# ------------------------------------------------------------------
# PATH SETUP & CONNECTIONS
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))

from config.data_connections import get_duckdb_connection

# ------------------------------------------------------------------
# DEFINIÇÃO DOS CONTRATOS (SCHEMAS)
# ------------------------------------------------------------------

class RawAtraso(pa.DataFrameModel):
    NUM_CPF: Series[str] = pa.Field(nullable=True)
    DAT_REFERENCIA: Series[str] = pa.Field(nullable=True)
    NUM_FATURA_HASH: Series[str] = pa.Field(nullable=True)
    NUM_ENT_SEQ_FATURA: Series[str] = pa.Field(nullable=True)
    CONTRATO: Series[str] = pa.Field(nullable=True)
    DW_UN_NEGOCIO: Series[str] = pa.Field(nullable=True)
    DW_HIS_PONTO_VENDA_COMTA: Series[str] = pa.Field(nullable=True)
    DW_NUM_CLIENTE: Series[str] = pa.Field(nullable=True)
    DW_AREA: Series[str] = pa.Field(nullable=True)
    DW_CICLO: Series[str] = pa.Field(nullable=True)
    DW_TIPO_CLIENTE_CONTA: Series[str] = pa.Field(nullable=True)
    DW_OFERTA: Series[str] = pa.Field(nullable=True)
    DW_FAIXA_AGING_FATURA: Series[str] = pa.Field(nullable=True)
    DW_FAIXA_AGING_DIVIDA: Series[str] = pa.Field(nullable=True)
    DW_FAIXA_TEMPO_BASE: Series[str] = pa.Field(nullable=True)
    DW_FAIXA_AGING_PROX_FECH: Series[str] = pa.Field(nullable=True)
    DW_TIPO_FATURAMENTO: Series[str] = pa.Field(nullable=True)
    COD_PLATAFORMA: Series[str] = pa.Field(nullable=True)
    DAT_CRIACAO_REGISTRO_TRANS: Series[str] = pa.Field(nullable=True)
    DAT_ALTERACAO_REGISTRO_TRANS: Series[str] = pa.Field(nullable=True)
    DAT_CANCELAMENTO_FAT: Series[str] = pa.Field(nullable=True)
    DAT_ORIGINAL_VCTO_FAT: Series[str] = pa.Field(nullable=True)
    DAT_ALTERACAO_VCTO_FAT: Series[str] = pa.Field(nullable=True)
    DAT_CRIACAO_FAT: Series[str] = pa.Field(nullable=True)
    DAT_VENCIMENTO_FAT: Series[str] = pa.Field(nullable=True)
    DAT_STATUS_FAT: Series[str] = pa.Field(nullable=True)
    DAT_MIN_VENCIMENTO_FAT: Series[str] = pa.Field(nullable=True)
    NUM_BILL_SEQ_FAT: Series[str] = pa.Field(nullable=True)
    NUM_SEQ_ACORDO_FAT: Series[str] = pa.Field(nullable=True)
    IND_ISENCAO_COB_FAT: Series[str] = pa.Field(nullable=True)
    IND_WO: Series[str] = pa.Field(nullable=True)
    IND_PDD: Series[str] = pa.Field(nullable=True)
    IND_PCCR: Series[str] = pa.Field(nullable=True)
    IND_ACA: Series[str] = pa.Field(nullable=True)
    IND_PRIMEIRA_FAT: Series[str] = pa.Field(nullable=True)
    IND_FRAUDE: Series[str] = pa.Field(nullable=True)
    VAL_FAT_LIQUIDO: Series[str] = pa.Field(nullable=True)
    VAL_FAT_BRUTO: Series[str] = pa.Field(nullable=True)
    VAL_FAT_CREDITO: Series[str] = pa.Field(nullable=True)
    VAL_FAT_AJUSTE: Series[str] = pa.Field(nullable=True)
    VAL_FAT_BRUTO_BC: Series[str] = pa.Field(nullable=True)
    VAL_FAT_PAGAMENTO_BRUTO: Series[str] = pa.Field(nullable=True)
    VAL_FAT_ABERTO: Series[str] = pa.Field(nullable=True)
    VAL_FAT_ABERTO_LIQ: Series[str] = pa.Field(nullable=True)
    VAL_MULTA_JUROS: Series[str] = pa.Field(nullable=True)
    VAL_MULTA_CANCELAMENTO: Series[str] = pa.Field(nullable=True)
    VAL_PARC_APARELHO_LIQ: Series[str] = pa.Field(nullable=True)
    VAL_FAT_LIQ_JM_MC: Series[str] = pa.Field(nullable=True)
    DAT_ATIVACAO_CONTA_CLI: Series[str] = pa.Field(nullable=True)
    DAT_CRIACAO_DW: Series[str] = pa.Field(nullable=True)

    class Config:
        strict = True
        coerce = True

raw_dados_cadastrais_schema = pa.DataFrameSchema(
    columns={
        "NUM_CPF": pa.Column(str, nullable=True),
        "SAFRA": pa.Column(str, nullable=True),
        "FLAG_INSTALACAO": pa.Column(str, nullable=True),
        "FPD": pa.Column(str, nullable=True),
        "PROD": pa.Column(str, nullable=True),
        "flag_mig2": pa.Column(str, nullable=True),
        "STATUSRF": pa.Column(str, nullable=True),
        "DATADENASCIMENTO": pa.Column(str, nullable=True),
        **{f"var_{i:02d}": pa.Column(str, nullable=True) for i in range(2, 26)},
        "CEP_3_digitos": pa.Column(str, nullable=True),
    },
    strict=True
)

class RawPagamento(pa.DataFrameModel):
    NUM_CPF: Series[str] = pa.Field(nullable=True)
    DAT_STATUS_FATURA: Series[str] = pa.Field(nullable=True)
    CONTRATO: Series[str] = pa.Field(nullable=True)
    SEQ_FATURA: Series[str] = pa.Field(nullable=True)
    NUM_SUB_SEQ_FATURA: Series[str] = pa.Field(nullable=True)
    NUM_CREDITO_SEQ: Series[str] = pa.Field(nullable=True)
    DW_TIPO_FATURA: Series[str] = pa.Field(nullable=True)
    IND_STATUS_FATURA: Series[str] = pa.Field(nullable=True)
    DW_NUM_CLIENTE: Series[str] = pa.Field(nullable=True)
    DW_AREA: Series[str] = pa.Field(nullable=True)
    DW_UN_NEGOCIO: Series[str] = pa.Field(nullable=True)
    DW_FORMA_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    VAL_PAGAMENTO_FATURA: Series[str] = pa.Field(nullable=True)
    DAT_CRIACAO_DW: Series[str] = pa.Field(nullable=True)
    DW_BANCO: Series[str] = pa.Field(nullable=True)
    DW_TIPO_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    NUM_BANCO_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    NUM_AGENCIA_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    NUM_CC_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    DW_MOTIVO_ESTORNO: Series[str] = pa.Field(nullable=True)
    VAL_DESCONTO_ITEM: Series[str] = pa.Field(nullable=True)
    VAL_PAGAMENTO_ITEM: Series[str] = pa.Field(nullable=True)
    VAL_JUROS_MULTAS_ITEM: Series[str] = pa.Field(nullable=True)
    VAL_MULTA_EQUIP_ITEM: Series[str] = pa.Field(nullable=True)
    VAL_MULTA_EQUIP_TOTAL: Series[str] = pa.Field(nullable=True)
    VAL_MULTA_FID_ITEM: Series[str] = pa.Field(nullable=True)
    COD_ORIGEM_NETUNO: Series[str] = pa.Field(nullable=True)
    COD_CONTA_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    SEQ_ENTIDADE_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    DAT_CRIACAO_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    DAT_ATUALIZACAO_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    COD_LOGIN_OPERADOR_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    COD_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    COD_RAZAO_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    DAT_BAIXA_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    VAL_BAIXA_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    DAT_DEPOSITO_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    COD_FUNDO_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    COD_BANCO_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    NUM_CONTA_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    COD_AGENCIA_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    SEQ_ENTIDADE_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    DAT_CRIACAO_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    DAT_ATUALIZACAO_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    COD_LOGIN_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    COD_FORMA_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    VAL_ORIGINAL_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    NUM_FATURA_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    COD_TIPO_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    DSC_NOME_BANCO_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    SEQ_ARQUIVO_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    NUM_PARCELA_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    NUM_AGRUPADOR_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    DSC_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    VAL_BAIXA_ATIVIDADE: Series[str] = pa.Field(nullable=True)
    VAL_ATUAL_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    COD_METODO_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    IND_STATUS_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    DAT_STATUS_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    COD_ARQUIVO_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    COD_NETUNO_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    DAT_CRIACAO_CREDITO: Series[str] = pa.Field(nullable=True)
    DAT_ATUALIZACAO_CREDITO: Series[str] = pa.Field(nullable=True)
    COD_LOGIN_CREDITO: Series[str] = pa.Field(nullable=True)
    VAL_PAGAMENTO_CREDITO: Series[str] = pa.Field(nullable=True)
    IND_TIPO_CREDITO: Series[str] = pa.Field(nullable=True)
    SEQ_PAGAMENTO_CREDITO: Series[str] = pa.Field(nullable=True)
    SEQ_FATURA_CREDITO: Series[str] = pa.Field(nullable=True)
    COD_ALOCACAO_CREDITO: Series[str] = pa.Field(nullable=True)
    COD_DESALOCACAO_CREDITO: Series[str] = pa.Field(nullable=True)
    SEQ_ENTIDADE_CREDITO: Series[str] = pa.Field(nullable=True)
    COD_TIPO_FATURA: Series[str] = pa.Field(nullable=True)
    DAT_ATIVIDADE_CREDITO: Series[str] = pa.Field(nullable=True)
    DAT_VENCIMENTO_CREDITO: Series[str] = pa.Field(nullable=True)

    class Config:
        strict = True

class RawRecarga(pa.DataFrameModel):
    NUM_CPF: Series[str] = pa.Field(nullable=True)
    DW_NUM_NTC: Series[str] = pa.Field(nullable=True)
    DAT_INSERCAO_CREDITO: Series[str] = pa.Field(nullable=True)
    HOR_INSERCAO_CREDITO: Series[str] = pa.Field(nullable=True)
    DW_NUM_CLIENTE: Series[str] = pa.Field(nullable=True)
    COD_TECNOLOGIA_DW: Series[str] = pa.Field(nullable=True)
    COD_CANAL_AQUISICAO: Series[str] = pa.Field(nullable=True)
    COD_TIPO_CREDITO: Series[str] = pa.Field(nullable=True)
    COD_PROMOCAO: Series[str] = pa.Field(nullable=True)
    VAL_CREDITO_INSERIDO: Series[str] = pa.Field(nullable=True)
    VAL_BONUS: Series[str] = pa.Field(nullable=True)
    VAL_REAL: Series[str] = pa.Field(nullable=True)
    COD_PLATAFORMA_ATU: Series[str] = pa.Field(nullable=True)
    COD_STATUS_PLATAFORMA: Series[str] = pa.Field(nullable=True)
    IND_METODO_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    DW_PLANO_TARIFACAO: Series[str] = pa.Field(nullable=True)
    DW_TIPO_RECARGA: Series[str] = pa.Field(nullable=True)
    DW_TIPO_INSERCAO: Series[str] = pa.Field(nullable=True)
    DW_FORMA_PAGAMENTO: Series[str] = pa.Field(nullable=True)
    DW_INSTITUICAO: Series[str] = pa.Field(nullable=True)
    COD_GRUPO_CARTAO: Series[str] = pa.Field(nullable=True)
    DSC_GRUPO_CARTAO_WPP: Series[str] = pa.Field(nullable=True)
    FLAG_SOS: Series[str] = pa.Field(nullable=True)
    VALOR_SOS: Series[str] = pa.Field(nullable=True)

    class Config:
        strict = True

class RawScore(pa.DataFrameModel):
    SAFRA: Series[str] = pa.Field(nullable=True)
    FLAG_INSTALACAO: Series[str] = pa.Field(nullable=True)
    FPD: Series[str] = pa.Field(nullable=True)
    PROD: Series[str] = pa.Field(nullable=True)
    flag_mig2: Series[str] = pa.Field(nullable=True)
    SCORE_01: Series[str] = pa.Field(nullable=True)
    SCORE_02: Series[str] = pa.Field(nullable=True)
    NUM_CPF: Series[str] = pa.Field(nullable=True)

    class Config:
        strict = True

raw_telco_schema = pa.DataFrameSchema(
    columns={
        "NUM_CPF": pa.Column(str, nullable=True),
        "SAFRA": pa.Column(str, nullable=True),
        "FLAG_INSTALACAO": pa.Column(str, nullable=True),
        "FPD": pa.Column(str, nullable=True),
        "PROD": pa.Column(str, nullable=True),
        "flag_mig2": pa.Column(str, nullable=True),
        **{f"var_{i:02d}": pa.Column(str, nullable=True) for i in range(26, 94)},
    },
    strict=True
)

# ------------------------------------------------------------------
# EXECUTOR DE VALIDAÇÃO
# ------------------------------------------------------------------

def run_contract_validation():
    con = get_duckdb_connection()
    log_path = PROJECT_ROOT / "reports/observability/quality/pandera/raw-schema_report-quality.log"
    os.makedirs(log_path.parent, exist_ok=True)

    targets = {
        "atraso": {"path": "s3://lake/raw/atraso/*.parquet", "contract": RawAtraso},
        "dados_cadastrais": {"path": "s3://lake/raw/dados_cadastrais/*.parquet", "contract": raw_dados_cadastrais_schema},
        "pagamento": {"path": "s3://lake/raw/pagamento/*.parquet", "contract": RawPagamento},
        "recarga": {"path": "s3://lake/raw/recarga/*.parquet", "contract": RawRecarga},
        "score_bureau_movel": {"path": "s3://lake/raw/score_bureau_movel/*.parquet", "contract": RawScore},
        "telco": {"path": "s3://lake/raw/telco/*.parquet", "contract": raw_telco_schema},
    }

    with open(log_path, "w", encoding="utf-8") as report:
        report.write(f"📋 RAW DATA CONTRACT AUDIT | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write("="*80 + "\n")
        report.write(f"{'STATUS':<10} | {'COLS':<5} | {'DETALHE'}\n")
        report.write("-"*80 + "\n")

        for table, cfg in targets.items():
            print(f"🔍 Auditando: {table}")
            
            if hasattr(cfg['contract'], "to_schema"):
                num_cols = len(cfg['contract'].to_schema().columns)
            else:
                num_cols = len(cfg['contract'].columns)

            try:
                df = con.execute(f"SELECT * FROM read_parquet('{cfg['path']}') LIMIT 100").df()
                cfg['contract'].validate(df)
                status = "✅ PASS"
                detail = f"Tabela '{table}' em conformidade."
            except Exception as e:
                status = "❌ FAIL"
                detail = f"Tabela '{table}' violou o contrato: {str(e)[:100]}..."
            
            log_line = f"{status:<9} | {num_cols:<5} | {detail}"
            print(log_line)
            report.write(log_line + "\n")

    print(f"🏁 Auditoria concluída. Relatório persistido em: {log_path}")

if __name__ == "__main__":
    run_contract_validation()