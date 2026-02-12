import json
import sys
import os
import re

def create_execution_json(run_id, operador, tempo_total, log_path):
    steps = []

    if os.path.exists(log_path):
        with open(log_path, 'r', encoding="utf-8") as f:
            for line in f:

                if "[SUCCESS]" in line:

                    # ---------------------------
                    # STEP NAME
                    # ---------------------------
                    parts = line.split('|')
                    step_name = parts[2].strip() if len(parts) > 2 else "UNKNOWN"
                    clean_name = step_name.split('  ')[0].strip()

                    # ---------------------------
                    # DURAÇÃO (HH:MM:SS)
                    # ---------------------------
                    duration_match = re.search(r'Duração:\s*([\d:]+)', line)
                    duration = duration_match.group(1) if duration_match else "N/I"

                    # ---------------------------
                    # STATUS 
                    # ---------------------------
                    status = "✅ OK"

                    steps.append({
                        "step": clean_name,
                        "status": status,
                        "duration": duration
                    })

    else:
        print(f"Log não encontrado em: {log_path}")

    # ---------------------------
    # MONTAGEM DO JSON FINAL
    # ---------------------------
    data = {
        "report_type": "Pipeline Execution",
        "title": "Sumário de Execução do Pipeline",
        "timestamp": f"{run_id[:4]}-{run_id[4:6]}-{run_id[6:8]}",
        "run_id": run_id,
        "operador": operador,
        "tempo_total": tempo_total,
        "steps": steps
    }

    # ---------------------------
    # OUTPUT
    # ---------------------------
    out_dir = "reports/observability"
    os.makedirs(out_dir, exist_ok=True)

    output_path = f"{out_dir}/pipeline_execution.json"

    with open(output_path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"JSON de execução criado com sucesso em: {output_path}")


if __name__ == "__main__":
    create_execution_json(
        sys.argv[1],  # run_id
        sys.argv[2],  # operador
        sys.argv[3],  # tempo_total
        sys.argv[4]   # log_path
    )
