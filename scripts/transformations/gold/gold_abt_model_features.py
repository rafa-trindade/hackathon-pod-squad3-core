import sys
import os
import pandas as pd
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
SOURCE_TABLE = "abt_base_cmv"
TARGET_TABLE = "abt_model_features" 

SOURCE_PATH = f"s3://lake/gold/{SOURCE_TABLE}/**/*.parquet"
RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d")
GOLD_BASE_PATH = f"gold/{TARGET_TABLE}/"
GOLD_PATH = f"s3://lake/{GOLD_BASE_PATH}run_id={RUN_ID}/"

QUALITY_REPORT_PATH = PROJECT_ROOT / "reports" / "observability" / "quality" / "pipeline" / f"gold-{TARGET_TABLE}-quality.log"

MAX_GOLD_RUNS = int(os.getenv("GOLD_MAX_RUNS", 2))


COLS_NECESSARIAS = [
    # Chaves e Metadados
    'num_cpf', 'safra', 'prod', 'fpd', 'flag_instalacao', 'ano_mes',
    
    # Bureau
    'bur_score_01', 'bur_score_02',
    
    # Cadastrais
    'tempo_conta_dias', 'idade', 'cad_datadenascimento', 'cad_cep_3_digitos',
    'cad_var_05', 'cad_var_16', 'cad_bureau_x_estabilidade',
    
    # Telco
    'tel_var_41', 'tel_var_33', 'tel_var_34', 
    'tel_var_31', 'tel_var_30', 'tel_var_28',
    'tel_var_48', 'tel_var_50', 'tel_var_82',
    
    # Recarga 
    'rec_qtd_geral', 'rec_qtd_l30d', 'rec_share_status_ativo', 'rec_qtd_plat_autoc',
    'rec_qtd_l90d', 'rec_vlr_total_geral', 'rec_vlr_total_l30d', 'rec_taxa_cartao_online',
    'rec_vlr_total_l60d', 'rec_vlr_total_l90d', 'rec_tendencia_vlr_l30_l90',
    'rec_qtd_sos_geral', 'rec_vlr_sos_l90d', 'rec_qtd_canais_digitais_geral', 
    'rec_dias_desde_ultima', 'rec_vlr_std_l90d', 'rec_vlr_bonus_geral',
    'rec_qtd_plano_controle_geral', 'rec_dependencia_sos', 'rec_share_digital', 
    'rec_share_bonus', 'rec_volatilidade_ticket', 'rec_indice_concentracao',
    'rec_indice_estresse_financeiro', 'rec_vlr_bonus_l90d',

    # Pagamento
    'pag_vlr_total_geral', 'pag_ticket_medio_geral', 'pag_qtd_debito_direto_geral', 
    'pag_qtd_faturas_geral', 'pag_qtd_faturas_l90d', 'pag_taxa_fatura_aberta',
    'pag_media_dias_atraso_l90d', 'pag_share_faturas_com_juros_geral', 'pag_esforco', 
    'pag_dias_desde_ultimo_pagamento', 'pag_vs_recarga_total',  'atr_vlr_acumulado_geral',
    'pag_instabilidade_pagamento',
    
    # Atraso
    'atr_vlr_max_geral', 'atr_qtd_faturas_atrasadas_geral', 'atr_dias_desde_ultimo_atraso',
    'atr_max_aging_divida_geral', 'atr_max_aging_divida_l90d', 'atr_intensidade', 'atr_fator_cronico',
    'atr_indice_gravidade_historica'
]

def run():
    con = get_duckdb_connection()
    con.execute("SET preserve_insertion_order = false")
    
    WORK_DB_PATH = f"/mnt/nvme/duckdb_temp/work_{TARGET_TABLE}.db"
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)
    con.execute(f"ATTACH '{WORK_DB_PATH}' AS work_db")

    print("--------------------------------------------------")
    print(f"🚀 Iniciando Gold Serving Layer: {TARGET_TABLE}")
    print(f"🎯 Etapa 1: Lendo ABT Bruta e extraindo Features Vitais...")

    cols_formatadas = ",\n        ".join(COLS_NECESSARIAS)

    con.execute(f"""
        CREATE TABLE work_db.lean_abt AS
        SELECT 
            {cols_formatadas}
        FROM read_parquet('{SOURCE_PATH}')
    """)

    # ------------------------------------------------------------------
    # ETAPA 2: AUDITORIA DE INTEGRIDADE E RELATÓRIO TÉCNICO
    # ------------------------------------------------------------------
    print("📊 Etapa 2: Gerando métricas de integridade da Serving Layer...")
    
    stats = con.execute("SELECT COUNT(*), COUNT(DISTINCT num_cpf) FROM work_db.lean_abt").fetchone()
    total_rows, total_cpfs = stats
    num_features = len(COLS_NECESSARIAS)

    report_log = f"📋 GOLD SERVING REPORT - {TARGET_TABLE} | RUN: {RUN_ID}\n"
    report_log += "="*100 + "\n"
    report_log += f"🏆 STATUS GERAL: ✅ SUCCESS | VARIÁVEIS: {num_features} colunas | REGISTROS: {total_rows:,} | CPFs ÚNICOS: {total_cpfs:,}\n".replace(",", ".")
    report_log += "="*100 + "\n\n"
    report_log += f"Esta tabela é uma view otimizada da {SOURCE_TABLE}, contendo estritamente as variáveis necessárias para inferência do CatBoost e renderização do Painel Streamlit.\n\n"
    
    print(report_log)
    
    os.makedirs(QUALITY_REPORT_PATH.parent, exist_ok=True)
    with open(QUALITY_REPORT_PATH, "w") as f: 
        f.write(report_log)

    # ------------------------------------------------------------------
    # ETAPA 3: ESCRITA E RETENÇÃO NO S3
    # ------------------------------------------------------------------
    print(f"💾 Etapa 3: Salvando dados otimizados particionados no Lake...")
    con.execute(f"""
        COPY (SELECT * FROM work_db.lean_abt) 
        TO '{GOLD_PATH}' 
        (FORMAT PARQUET, PARTITION_BY (ano_mes), OVERWRITE_OR_IGNORE 1)
    """)    
    
    con.execute("DETACH work_db")
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)
    
    cleanup_old_runs(bucket="lake", base_path=GOLD_BASE_PATH, max_runs=MAX_GOLD_RUNS, protect_run_id=RUN_ID)
    print(f"🏁 Serving ABT persistida em: {GOLD_PATH}")
    print("--------------------------------------------------")

if __name__ == "__main__":
    run()