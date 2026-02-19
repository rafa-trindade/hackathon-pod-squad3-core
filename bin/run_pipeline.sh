#!/usr/bin/env bash
#chmod +x bin/run_pipeline.sh
#
# ==============================================================================
# ORQUESTRADOR DO PIPELINE DE DADOS (SQUAD 3)
# ==============================================================================
# Este script é responsável por orquestrar a execução sequencial de todas as
# etapas do pipeline de dados, seguindo a arquitetura Medallion (Raw -> Gold).
#
# Funcionalidades principais:
# 1. Rastreabilidade e Logs: Gera logs estruturados (com timestamp, níveis de 
#    severidade e duração) salvos em 'bin/reports/pipeline_execution.log'.
# 2. Execução Segura (Fail-Fast): Utiliza 'set -euo pipefail' para garantir que 
#    o pipeline seja interrompido imediatamente em caso de falha crítica em 
#    qualquer etapa, evitando propagação de dados incorretos.
# 3. Gestão de Camadas: 
#    - RAW: Validação de contratos (Quality) e Profiling.
#    - BRONZE: Transformação básica, Profiling e Inspeção de partições.
#    - SILVER: Refinamento, Profiling e Inspeção.
#    - GOLD: Geração de features/ABTs, Labels FPD e Profiling final.
# 4. Observabilidade e Relatórios: Ao final do processamento, extrai o tempo 
#    total, gera um relatório JSON da execução e faz o upload (parse e envio) 
#    para alimentar os painéis de observabilidade.
# ==============================================================================

set -euo pipefail

#########################################
# CONFIG
#########################################
RUN_ID=$(date +"%Y%m%d")
LOG_DIR="bin/reports"
LOG_FILE="${LOG_DIR}/pipeline_execution.log"
PYTHON_BIN=python

export RUN_ID_PIPELINE="${RUN_ID}"
export LOG_FILE_PATH="${LOG_FILE}"
export DISABLE_PANDERA_IMPORT_WARNING=True

mkdir -p "$LOG_DIR"
> "$LOG_FILE"

#########################################
# UTILS & FORMATTING
#########################################
format_time() {
  local T_MS=$1
  local T_S=$((T_MS / 1000))
  printf '%02d:%02d:%02d' $((T_S/3600)) $((T_S%3600/60)) $((T_S%60))
}

log() {
  local LEVEL=$1
  local MSG=$2
  local TS
  TS="$(date '+%Y-%m-%d %H:%M:%S')"
  
  local LINE
  LINE=$(printf "%-19s | %-10s | %s" "$TS" "[$LEVEL]" "$MSG")

  echo "$LINE"
  echo "$LINE" >> "$LOG_FILE"
}

separator() {
  local SEP="============================================================================================================="
  echo "$SEP"
  echo "$SEP" >> "$LOG_FILE"
}

#########################################
# STEP RUNNER
#########################################
run_step() {
  local NAME=$1
  local MODULE=$2
  local START END ELAPSED_MS TIME_STR

  log "PROCESS" "$(printf "%-40s | Iniciando..." "${NAME}")"
  
  START=$(date +%s%3N)

  if $PYTHON_BIN -m "$MODULE" 1>/dev/null 2>>"$LOG_FILE"; then
    END=$(date +%s%3N)
    ELAPSED_MS=$((END - START))
    TIME_STR=$(format_time "$ELAPSED_MS")

    local FINAL_MSG
    FINAL_MSG=$(printf "%-40s | Status: OK | Duração: %s" "${NAME}" "${TIME_STR}")
    
    log "SUCCESS" "$FINAL_MSG"
    echo "-------------------------------------------------------------------------------------------------------------" >> "$LOG_FILE"
  else
    log "ERROR" "$(printf "%-40s | FALHA CRÍTICA" "${NAME}")"
    exit 1
  fi
}

#########################################
# HEADER DE EXECUÇÃO 
#########################################
clear
separator
log "START" "DATA PIPELINE EXECUTION - SQUAD 3"
log "INFO"  "RUN_ID:   $RUN_ID"
log "INFO"  "OPERADOR: $(whoami)"
log "INFO"  "HOST:     $(hostname)"
log "INFO"  "LOG FILE: $LOG_FILE"
separator

PIPELINE_START=$(date +%s%3N)

######################################### 
# 0. QUALITY RAW 
######################################### 
run_step "QUALITY RAW" "scripts.quality.contracts.raw_contract"

#########################################
# 1. PROFILING - RAW
#########################################
run_step "PROFILING RAW - atraso_dim" "scripts.profiling.raw.profile_atraso_dim"
run_step "PROFILING RAW - atraso" "scripts.profiling.raw.profile_atraso"
run_step "PROFILING RAW - dados_cadastrais" "scripts.profiling.raw.profile_dados_cadastrais"
run_step "PROFILING RAW - pagamento" "scripts.profiling.raw.profile_pagamento"
run_step "PROFILING RAW - recarga_dim" "scripts.profiling.raw.profile_recarga_dim"
run_step "PROFILING RAW - recarga" "scripts.profiling.raw.profile_recarga"
run_step "PROFILING RAW - score_bureau" "scripts.profiling.raw.profile_score_bureau_movel"
run_step "PROFILING RAW - telco" "scripts.profiling.raw.profile_telco"

#########################################
# 2. TRANSFORMING - BRONZE
#########################################
run_step "BRONZE - atraso" "scripts.transformations.bronze.bronze_atraso"
run_step "BRONZE - atraso_dim" "scripts.transformations.bronze.bronze_atraso_dim"
run_step "BRONZE - dados_cadastrais" "scripts.transformations.bronze.bronze_dados_cadastrais"
run_step "BRONZE - pagamento" "scripts.transformations.bronze.bronze_pagamento"
run_step "BRONZE - recarga" "scripts.transformations.bronze.bronze_recarga"
run_step "BRONZE - recarga_dim" "scripts.transformations.bronze.bronze_recarga_dim"
run_step "BRONZE - score_bureau" "scripts.transformations.bronze.bronze_score_bureau_movel"
run_step "BRONZE - telco" "scripts.transformations.bronze.bronze_telco"

#########################################
# 3. PROFILING & INSPECTION - BRONZE
#########################################
run_step "PROFILING BRONZE - atraso_dim" "scripts.profiling.bronze.profile_atraso_dim"
run_step "PROFILING BRONZE - atraso" "scripts.profiling.bronze.profile_atraso"
run_step "PROFILING BRONZE - dados_cadastrais" "scripts.profiling.bronze.profile_dados_cadastrais"
run_step "PROFILING BRONZE - pagamento" "scripts.profiling.bronze.profile_pagamento"
run_step "PROFILING BRONZE - recarga_dim" "scripts.profiling.bronze.profile_recarga_dim"
run_step "PROFILING BRONZE - recarga" "scripts.profiling.bronze.profile_recarga"
run_step "PROFILING BRONZE - score_bureau" "scripts.profiling.bronze.profile_score_bureau_movel"
run_step "PROFILING BRONZE - telco" "scripts.profiling.bronze.profile_telco"
run_step "INSPECT BRONZE" "scripts.transformations.utils.inspect_partition_bronze"

#########################################
# 4. TRANSFORMING - SILVER
#########################################
run_step "SILVER - atraso" "scripts.transformations.silver.silver_atraso"
run_step "SILVER - dados_cadastrais" "scripts.transformations.silver.silver_dados_cadastrais"
run_step "SILVER - pagamento" "scripts.transformations.silver.silver_pagamento"
run_step "SILVER - recarga" "scripts.transformations.silver.silver_recarga"
run_step "SILVER - score_bureau" "scripts.transformations.silver.silver_score_bureau_movel"
run_step "SILVER - telco" "scripts.transformations.silver.silver_telco"

#########################################
# 5. PROFILING & INSPECTION - SILVER
#########################################
run_step "PROFILING SILVER - atraso" "scripts.profiling.silver.profile_atraso"
run_step "PROFILING SILVER - dados_cadastrais" "scripts.profiling.silver.profile_dados_cadastrais"
run_step "PROFILING SILVER - pagamento" "scripts.profiling.silver.profile_pagamento"
run_step "PROFILING SILVER - recarga" "scripts.profiling.silver.profile_recarga"
run_step "PROFILING SILVER - score_bureau" "scripts.profiling.silver.profile_score_bureau_movel"
run_step "PROFILING SILVER - telco" "scripts.profiling.silver.profile_telco"
run_step "INSPECT SILVER" "scripts.transformations.utils.inspect_partition_silver"

#########################################
# 6. TRANSFORMING - GOLD
#########################################
run_step "GOLD - labels_fpd" "scripts.transformations.gold.gold_labels_fpd"
run_step "GOLD - abt_base_prod" "scripts.transformations.gold.gold_abt_base_prod"
run_step "GOLD - labels_fpd_bureau" "scripts.transformations.gold.gold_labels_fpd_bureau"
run_step "GOLD - abt_base_cmv" "scripts.transformations.gold.gold_abt_base_cmv"

#########################################
# 7. PROFILING & INSPECTION - GOLD
#########################################
run_step "PROFILING GOLD - labels_fpd" "scripts.profiling.gold.profile_labels_fpd"
run_step "PROFILING GOLD - abt_base_prod" "scripts.profiling.gold.profile_abt_base_prod"
run_step "PROFILING GOLD - labels_fpd_bureau" "scripts.profiling.gold.profile_labels_fpd_bureau"
run_step "PROFILING GOLD - abt_base_cmv" "scripts.profiling.gold.profile_abt_base_cmv"
run_step "INSPECT GOLD" "scripts.transformations.utils.inspect_partition_gold"

#########################################
# FOOTER FINAL
#########################################
PIPELINE_END=$(date +%s%3N)
TOTAL_MS=$((PIPELINE_END - PIPELINE_START))
TOTAL_TIME_STR=$(format_time "$TOTAL_MS")

separator
log "END" "PIPELINE FINALIZADA COM SUCESSO"
log "END" "TEMPO TOTAL: ${TOTAL_TIME_STR}"
separator

#########################################
# UPLOAD OBSERVABILITY REPORTS
#########################################
echo "Gerando JSON de execução..."
$PYTHON_BIN scripts/observability/generate_pipeline_report.py "$RUN_ID" "$(whoami)" "$TOTAL_TIME_STR" "$LOG_FILE"

run_step "PARSE OBSERVABILITY REPORTS" "scripts.observability.parse_reports"

run_step "UPLOAD OBSERVABILITY REPORTS" "scripts.transformations.utils.upload_observability_reports"