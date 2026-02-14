import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from botocore.config import Config

# ------------------------------------------------------------------
# PATH SETUP
# ------------------------------------------------------------------
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
except IndexError:
    PROJECT_ROOT = Path(".").resolve()

sys.path.append(str(PROJECT_ROOT))

try:
    from config.data_connections import get_s3_client
    from scripts.transformations.utils.lake_retention import cleanup_old_runs
except ImportError:
    def get_s3_client():
        import boto3

        config = Config(
            request_checksum_calculation="when_required",
            response_checksum_validation="when_required"
        )
        return boto3.client("s3", config=config)
    
    def cleanup_old_runs(**kwargs):
        print(f"Limpando runs antigos: {kwargs}")

# ------------------------------------------------------------------
# CONFIGURAÇÕES
# ------------------------------------------------------------------
RUN_ID = os.getenv("RUN_ID_PIPELINE", datetime.now(timezone.utc).strftime("%Y%m%d"))
CURRENT_LOG_FILE = os.getenv("LOG_FILE_PATH")

LOCAL_REPORTS_PATH = PROJECT_ROOT / "reports" / "observability"
LAKE_BUCKET = "lake"
LAKE_BASE_PREFIX = "observability/reports/"
LAKE_DEST_PATH = f"{LAKE_BASE_PREFIX}run_id={RUN_ID}"

MAX_REPORTS_RUNS = int(os.getenv("REPORTS_MAX_RUNS", 1))

def upload_reports():
    """
    Faz o upload recursivo dos relatórios e do log principal da execução para o S3.
    """

    s3_client = get_s3_client()
    
    print("--------------------------------------------------")
    print(f"📡 Iniciando Sincronização de Observabilidade (Fix: Compatibility Mode)")
    print(f"🧾 run_id = {RUN_ID}")
    
    files_count = 0

    if LOCAL_REPORTS_PATH.exists():
        for root, dirs, files in os.walk(LOCAL_REPORTS_PATH):
            for file in files:
                local_file_path = Path(root) / file
                
                if local_file_path.stat().st_size == 0 or file.startswith("."):
                    continue

                relative_path = local_file_path.relative_to(LOCAL_REPORTS_PATH)
                s3_key = f"{LAKE_DEST_PATH}/{relative_path}"
                
                try:
                    s3_client.upload_file(str(local_file_path), LAKE_BUCKET, s3_key)
                    files_count += 1
                except Exception as e:
                    print(f"⚠️ Erro ao subir {relative_path}: {e}")

    if CURRENT_LOG_FILE and os.path.exists(CURRENT_LOG_FILE):
        log_name = os.path.basename(CURRENT_LOG_FILE) 
        s3_log_key = f"{LAKE_DEST_PATH}/{log_name}"
        
        try:
            s3_client.upload_file(CURRENT_LOG_FILE, LAKE_BUCKET, s3_log_key)
            print(f"📄 Log principal consolidado: {log_name}")
            files_count += 1
        except Exception as e:
            print(f"⚠️ Erro ao subir log principal: {e}")

    print(f"✅ Sucesso! {files_count} arquivos sincronizados.")
    print(f"📍 Destino: s3://{LAKE_BUCKET}/{LAKE_DEST_PATH}/")

    print(f"🧹 Aplicando política de retenção (Max: {MAX_REPORTS_RUNS} runs)...")
    try:
        cleanup_old_runs(
            bucket=LAKE_BUCKET,
            base_path=LAKE_BASE_PREFIX,
            max_runs=MAX_REPORTS_RUNS,
            protect_run_id=RUN_ID,
        )
    except Exception as e:
        print(f"⚠️ Falha na limpeza: {e}")

    print("--------------------------------------------------")

if __name__ == "__main__":
    upload_reports()