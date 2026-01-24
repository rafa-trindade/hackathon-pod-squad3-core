import sys
import os
from pathlib import Path
from datetime import datetime
import contextlib

# ------------------------------------------------------------------
# PATH SETUP
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))

from config.data_connections import get_duckdb_connection

# ------------------------------------------------------------------
# CONFIGURAÇÃO DE LOG
# ------------------------------------------------------------------
LOG_DIR = PROJECT_ROOT / "reports" / "observability" / "integrity"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "inspect_partition-gold.log"

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open(LOG_FILE, "w", encoding="utf-8")
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        self.terminal.flush()
        self.log.flush()

# ------------------------------------------------------------------
# CONFIGURAÇÃO INDIVIDUAL POR PASTA
# ------------------------------------------------------------------
TABLES_CONFIG = {
    "labels_fpd": {
        "col_date": "safra",
        "start": "202410",
        "end": "202503"
    },
    "abt_base_prod": {
        "col_date": "safra",
        "start": "202410",
        "end": "202503"
    }
}

def get_month_list(start_str, end_str):
    start_dt = datetime.strptime(start_str, "%Y%m")
    end_dt = datetime.strptime(end_str, "%Y%m")
    months = []
    current_dt = start_dt
    while current_dt <= end_dt:
        months.append(current_dt.strftime("%Y%m"))
        m = current_dt.month
        y = current_dt.year
        current_dt = datetime(y + (m // 12), (m % 12) + 1, 1)
    return months

def get_latest_run_id(con, table_name):
    try:
        path = f"s3://lake/gold/{table_name}/run_id=*/**/*.parquet"
        query = f"SELECT MAX(run_id) AS latest_rid FROM read_parquet('{path}', hive_partitioning=1)"
        res = con.execute(query).fetchone()
        return res[0] if res else None
    except:
        return None

def inspect_all():
    with contextlib.redirect_stdout(None):
        con = get_duckdb_connection()
    
    sys.stdout = Logger()
    
    timestamp_exec = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    periodos_globais = get_month_list("202310", "202503")

    print("\n" + "="*80)
    print(f"🕵️  AUDITORIA DE PARTIÇÕES GOLD - {timestamp_exec}")
    print(f"📂 Arquivo de Log: {LOG_FILE.relative_to(PROJECT_ROOT)}") 
    print("="*80)

    for table, cfg in TABLES_CONFIG.items():
        col_date = cfg["col_date"]
        print(f"\n📊 TABELA: {table.upper()}")
        
        run_id = get_latest_run_id(con, table)
        if not run_id:
            print(f"❌ Erro: Nenhuma run_id encontrada para {table}")
            continue
            
        periodos = get_month_list(cfg["start"], cfg["end"])
        print(f"🆔 Run ID: {run_id} | Coluna: {col_date}")
        print(f"📅 Janela: {cfg['start']} a {cfg['end']}")
        print("-" * 60)

        for periodo in periodos:
            path = f"s3://lake/gold/{table}/run_id={run_id}/ano_mes={periodo}/*.parquet"
            query = f"SELECT COUNT(*) as total, MIN({col_date}::DATE) as dt_min, MAX({col_date}::DATE) as dt_max FROM read_parquet('{path}')"

            try:
                res = con.execute(query).df()
                total = res['total'][0]
                if total > 0:
                    dt_min, dt_max = str(res['dt_min'][0]), str(res['dt_max'][0])
                    prefix = f"{periodo[:4]}-{periodo[4:]}"
                    status = "✅ OK" if dt_min.startswith(prefix) and dt_max.startswith(prefix) else "⚠️  DIVERGENTE"
                    print(f"  📁 {periodo}: {total:10,} linhas | Min: {dt_min} | Max: {dt_max} | {status}")
                else:
                    print(f"  📁 {periodo}: 📭 VAZIA")
            except:
                print(f"  📁 {periodo}: ❌ Pasta não encontrada")

    print("\n" + "="*80)
    print(f"🏁 Auditoria Finalizada.")
    print("="*80 + "\n")

    if isinstance(sys.stdout, Logger):
        sys.stdout.log.close()
        sys.stdout = sys.stdout.terminal

if __name__ == "__main__":
    inspect_all()