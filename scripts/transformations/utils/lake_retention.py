from typing import List
import re
import os
import boto3


def cleanup_old_runs(
    bucket: str,
    base_path: str,
    max_runs: int,
    protect_run_id: str | None = None,
) -> None:

    if max_runs <= 0:
        print("⚠️ max_runs <= 0 - nenhuma limpeza será aplicada")
        return

    # ------------------------------------------------------------
    # S3 client (MINIO)
    # ------------------------------------------------------------
    s3 = boto3.client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )

    paginator = s3.get_paginator("list_objects_v2")

    run_ids: set[str] = set()

    for page in paginator.paginate(Bucket=bucket, Prefix=base_path):
        for obj in page.get("Contents", []):
            match = re.search(r"run_id=([^/]+)/", obj["Key"])
            if match:
                run_ids.add(match.group(1))

    if not run_ids:
        print("ℹ️ Nenhuma run encontrada para limpeza")
        return

    # ------------------------------------------------------------
    # Ordena runs (mais recentes primeiro)
    # ------------------------------------------------------------
    sorted_runs = sorted(run_ids, reverse=True)

    # ------------------------------------------------------------
    # Define runs a manter
    # ------------------------------------------------------------
    runs_to_keep = sorted_runs[:max_runs]

    if protect_run_id and protect_run_id not in runs_to_keep:
        runs_to_keep.append(protect_run_id)

    runs_to_delete = [
        r for r in sorted_runs
        if r not in runs_to_keep
    ]

    if not runs_to_delete:
        print("ℹ️ Nenhuma run antiga para remover")
        return

    print(f"🗑️ Runs a remover: {runs_to_delete}")

    # ------------------------------------------------------------
    # Remove objetos
    # ------------------------------------------------------------
    for run_id in runs_to_delete:
        prefix = f"{base_path}run_id={run_id}/"
        print(f"🧹 Removendo {prefix}")

        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            objects = page.get("Contents", [])
            if not objects:
                continue

            s3.delete_objects(
                Bucket=bucket,
                Delete={
                    "Objects": [{"Key": obj["Key"]} for obj in objects],
                    "Quiet": True,
                },
            )

    print("✅ Limpeza de runs antigas concluída")