import sys
from pathlib import Path
from datetime import datetime

# ------------------------------------------------------------------
# PATH SETUP
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))

from config.data_connections import get_duckdb_connection

# --- CONFIGURAÇÃO DE ALVO
RUN_ID = "20260110_011720" 
TABLE_NAME = "dados_cadastrais"
COLUMN_DATE = "safra"

# --- CONFIGURAÇÃO DO PARTIÇÕES
START_PERIOD = "202410"
END_PERIOD   = "202503"  

def get_month_list(start_str, end_str):
    """Gera uma lista de strings YYYYMM entre o início e o fim."""
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

def inspect_all():
    con = get_duckdb_connection()
    periodos = get_month_list(START_PERIOD, END_PERIOD)

    print(f"🚀 Iniciando Inspeção em Lote: {TABLE_NAME}")
    print(f"📅 Período: {START_PERIOD} até {END_PERIOD}")
    print(f"🔑 Chave de conferência: {COLUMN_DATE}")
    print("=" * 80)

    for periodo in periodos:
        path = f"s3://lake/silver/{TABLE_NAME}/run_id={RUN_ID}/ano_mes={periodo}/*.parquet"
        
        query = f"""
            SELECT 
                COUNT(*) as total,
                MIN({COLUMN_DATE}::DATE) as dt_min,
                MAX({COLUMN_DATE}::DATE) as dt_max
            FROM read_parquet('{path}')
        """

        try:
            res = con.execute(query).df()
            total = res['total'][0]

            if total > 0:
                dt_min = str(res['dt_min'][0])
                dt_max = str(res['dt_max'][0])
                
                expected_prefix = f"{periodo[:4]}-{periodo[4:]}"
                status = "✅ OK" if dt_min.startswith(expected_prefix) and dt_max.startswith(expected_prefix) else "⚠️ ERRO"
                
                print(f"📁 Pasta {periodo}: {total:10,} linhas | Min: {dt_min} | Max: {dt_max} | {status}")
            else:
                print(f"📁 Pasta {periodo}: 📭 VAZIA")

        except Exception:

            print(f"📁 Pasta {periodo}: ❌ Pasta não encontrada no S3")

    print("=" * 80)
    print("🏁 Inspeção finalizada.")

if __name__ == "__main__":
    inspect_all()