import os
from urllib.parse import urlparse
from botocore.config import Config
from dotenv import load_dotenv
import boto3
import duckdb

load_dotenv(override=True)

# --------------------------------------------------------------
# MinIO/S3
# --------------------------------------------------------------
def get_minio_endpoint() -> str:
    return os.getenv("S3_ENDPOINT")


def get_s3_client():

    endpoint = get_minio_endpoint()
    if not endpoint:
        raise RuntimeError("S3_ENDPOINT não definido")

    s3_config = Config(
        #request_checksum_calculation="when_required",
        #response_checksum_validation="when_required"
    )

    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        config=s3_config
    )

# --------------------------------------------------------------
# DuckDB connection
# --------------------------------------------------------------
def get_duckdb_connection(
    memory_limit: str = None,
    threads: int = None,
) -> duckdb.DuckDBPyConnection:
    

    if memory_limit is None:
        memory_limit = os.getenv("DUCKDB_MEMORY_LIMIT", "26GB")
    
    if threads is None:
        threads = int(os.getenv("DUCKDB_THREADS", 6))

    con = duckdb.connect()

    # -----------------------------
    # MinIO endpoint
    # -----------------------------
    endpoint = get_minio_endpoint()
    if not endpoint:
        raise RuntimeError("S3_ENDPOINT não definido")

    parsed = urlparse(endpoint)
    if not parsed.netloc:
        raise RuntimeError(f"S3_ENDPOINT inválido: {endpoint}")

    duckdb_endpoint = parsed.netloc

    # ---------------------------------------------------------------
    # DuckDB temp directory (NVMe) 
    # ---------------------------------------------------------------
    temp_dir = "/mnt/nvme/duckdb_temp"
    if not os.path.isdir(temp_dir):
        raise RuntimeError(
            f"DuckDB temp_directory não existe ou não é diretório: {temp_dir}"
        )

    print(f"DuckDB memory_limit = {memory_limit}")
    print(f"DuckDB threads = {threads}")
    print(f"DuckDB temp_directory = {temp_dir}")
    print(f"DuckDB s3_endpoint = {duckdb_endpoint}")

    con.execute(f"""
        PRAGMA temp_directory='{temp_dir}';

        SET memory_limit='{memory_limit}';
        SET threads={threads};

        SET s3_endpoint='{duckdb_endpoint}';
        SET s3_access_key_id='{os.getenv("AWS_ACCESS_KEY_ID")}';
        SET s3_secret_access_key='{os.getenv("AWS_SECRET_ACCESS_KEY")}';
        SET s3_region='{os.getenv("AWS_DEFAULT_REGION", "us-east-1")}';
        SET s3_use_ssl=true;
        SET s3_url_style='path';
    """)

    return con