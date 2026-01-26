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
SOURCE_TABLE = "telco"
TARGET_TABLE = "labels_fpd"

SILVER_PATH = f"s3://lake/silver/{SOURCE_TABLE}/**/*.parquet"
RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
GOLD_BASE_PATH = f"gold/{TARGET_TABLE}/"
GOLD_PATH = f"s3://lake/{GOLD_BASE_PATH}run_id={RUN_ID}/"

QUALITY_REPORT_PATH = PROJECT_ROOT / "reports" / "observability" / "quality" / "pipeline" / f"gold-{TARGET_TABLE}-quality.log"

MAX_GOLD_RUNS = int(os.getenv("GOLD_MAX_RUNS", 1))

def run():
    con = get_duckdb_connection()
    con.execute("SET preserve_insertion_order = false")
    
    WORK_DB_PATH = f"/mnt/nvme/duckdb_temp/work_{TARGET_TABLE}.db"
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)
    con.execute(f"ATTACH '{WORK_DB_PATH}' AS work_db")

    print("--------------------------------------------------")
    print(f"🏆 Iniciando Gold: {TARGET_TABLE}")
    print(f"🧾 run_id = {RUN_ID}")
    
    # ------------------------------------------------------------------
    # ETAPA PREVIA: Auditoria de Origem (Silver)
    # ------------------------------------------------------------------
    silver_stats = con.execute(f"""
        SELECT 
            COUNT(*) as total, 
            COUNT(*) FILTER (WHERE fpd IS NULL) as nulos
        FROM read_parquet('{SILVER_PATH}')
    """).fetchone()
    
    silver_total = silver_stats[0]
    silver_nulos = silver_stats[1]

    # ------------------------------------------------------------------
    # ETAPA 1: Processamento da Label e Regras de Negócio
    # ------------------------------------------------------------------
    print("--------------------------------------------------")
    print("🎯 Etapa 1: Transformação e filtragem de Missings...")

    con.execute(f"""
        CREATE TABLE work_db.gold_step1 AS
        SELECT 
            num_cpf,
            safra,
            prod,
            fpd,
            flag_instalacao,
            ano_mes,
            '{RUN_ID}' AS run_id,
            now() AS ingestion_ts
        FROM read_parquet('{SILVER_PATH}')
        WHERE fpd IS NOT NULL
        QUALIFY ROW_NUMBER() OVER(
            PARTITION BY num_cpf, safra, prod 
            ORDER BY ingestion_ts DESC
        ) = 1
    """)

    gold_count = con.execute("SELECT COUNT(*) FROM work_db.gold_step1").fetchone()[0]

    # ------------------------------------------------------------------
    # ETAPA 2: Bateria de Testes de Qualidade (Data Quality)
    # ------------------------------------------------------------------
    print("--------------------------------------------------")
    print("🧪 Etapa 2: Executando bateria de testes e Overlap...")
    
    test_results = []

    # Teste 1: Unicidade no Grão
    dup_check = con.execute("""
        SELECT COUNT(*) - COUNT(DISTINCT (num_cpf || safra || prod)) 
        FROM work_db.gold_step1
    """).fetchone()[0]
    test_results.append(["Unicidade no Grão", "PASS" if dup_check == 0 else "FAIL", f"{dup_check} duplicatas"])

    # Teste 2: % Missing = 0
    missing_check = con.execute("SELECT COUNT(*) FROM work_db.gold_step1 WHERE fpd IS NULL").fetchone()[0]
    test_results.append(["Missing FPD Gold = 0", "PASS" if missing_check == 0 else "FAIL", f"{missing_check} nulos"])

    # Teste 3: Distribuição por Safra
    dist_check = con.execute(f"""
        SELECT 
            strftime(safra, '%Y%m') as safra_fmt, 
            COUNT(*) * 100.0 / {gold_count} as pct_representatividade
        FROM work_db.gold_step1 
        GROUP BY 1 
        ORDER BY 1
    """).df()

    # Teste 4: Checagem de Overlap ---
    gold_unique_cpfs = con.execute("SELECT COUNT(DISTINCT num_cpf) FROM work_db.gold_step1").fetchone()[0]

    ORDERED_OVERLAP = ["dados_cadastrais", "score_bureau_movel", "atraso", "pagamento", "recarga"]
    overlap_results = []

    for table in ORDERED_OVERLAP:
        print(f"🔗 Cruzando Gold com Silver: {table}...")
        try:
            overlap_query = f"""
                WITH gold_keys AS (SELECT DISTINCT num_cpf FROM work_db.gold_step1),
                     silver_keys AS (SELECT DISTINCT num_cpf FROM read_parquet('s3://lake/silver/{table}/**/*.parquet'))
                SELECT COUNT(g.num_cpf) 
                FROM gold_keys g
                INNER JOIN silver_keys s ON g.num_cpf = s.num_cpf
            """
            matches = con.execute(overlap_query).fetchone()[0]
            pct = (matches / gold_unique_cpfs) if gold_unique_cpfs > 0 else 0
            status = "PASS" if pct >= 0.7 else "WARN"
            overlap_results.append([f"Overlap {table}", status, f"{pct:.2%} de match"])
        except Exception as e:
            overlap_results.append([f"Overlap {table}", "ERROR", "Falha ao ler tabela"])

    # ------------------------------------------------------------------
    # GERAÇÃO DO ARQUIVO DE LOG DE QUALIDADE
    # ------------------------------------------------------------------
    pct_missing_silver = (silver_nulos / silver_total) * 100 if silver_total > 0 else 0
    
    report_header = f"📋 QUALITY REPORT - {TARGET_TABLE} | RUN: {RUN_ID}\n"
    report_line = "-" * 82 + "\n"
    report_table_head = f"{'TESTE':<29} | {'STATUS':<10} | {'OBSERVAÇÃO'}\n"
    
    report_log = report_header + report_line + report_table_head + report_line
    
    report_log += f"{test_results[0][0]:<29} | {test_results[0][1]:<10} | {test_results[0][2]}\n"
    report_log += f"{test_results[1][0]:<29} | {test_results[1][1]:<10} | {test_results[1][2]}\n"
    
    report_log += report_line
    for row in dist_check.itertuples():
        # Regra: PASS entre 10.0% e 90.0%
        status_safra = "PASS" if 10.0 <= row.pct_representatividade <= 90.0 else "WARN"
        nome_teste = f"Distribuição Safra {row.safra_fmt}"
        report_log += f"{nome_teste:<29} | {status_safra:<10} | {row.pct_representatividade:.1f}%\n"
    report_log += report_line
    
    for r in overlap_results:
        report_log += f"{r[0]:<29} | {r[1]:<10} | {r[2]}\n"
        
    report_log += report_line
    report_log += f"{'Saneamento (Missing)':<29} | {'INFO':<10} | Descartados {silver_nulos:,} registros ({pct_missing_silver:.2f}%)\n"
    report_log += report_line

    os.makedirs(QUALITY_REPORT_PATH.parent, exist_ok=True)
    with open(QUALITY_REPORT_PATH, "w") as f:
        f.write(report_log)

    print("\n✅ Relatório de Qualidade salvo com sucesso.")
    print(report_log)

    if any(r[1] == "FAIL" for r in test_results[:2]):
        raise ValueError("❌ Falha crítica nos testes de qualidade. O processo foi interrompido.")

    # ------------------------------------------------------------------
    # ETAPA 3: Persistência
    # ------------------------------------------------------------------
    print("--------------------------------------------------")
    print(f"💾 Etapa 3: Gravando dados na GOLD (Run: {RUN_ID})...")
    
    con.execute(f"""
        COPY (SELECT * FROM work_db.gold_step1 ORDER BY ano_mes) 
        TO '{GOLD_PATH}' 
        (FORMAT PARQUET, PARTITION_BY (ano_mes), OVERWRITE_OR_IGNORE 1)
    """)
    
    # ------------------------------------------------------------------
    # ETAPA 4: Limpeza Final
    # ------------------------------------------------------------------
    con.execute("DETACH work_db")
    if os.path.exists(WORK_DB_PATH): os.remove(WORK_DB_PATH)

    print("--------------------------------------------------")
    print("🧹 Etapa 4: Aplicando política de retenção na Gold...")
    cleanup_old_runs(bucket="lake", base_path=GOLD_BASE_PATH, max_runs=MAX_GOLD_RUNS, protect_run_id=RUN_ID)

    print("--------------------------------------------------")
    print(f"🏁 Pipeline {TARGET_TABLE} Gold finalizado com sucesso!")

if __name__ == "__main__":
    run()