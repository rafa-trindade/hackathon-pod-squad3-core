#!/usr/bin/env bash
#chmod +x bin/manage_streamlit.sh
#
# ==============================================================================
# GERENCIADOR DE PAINÉIS STREAMLIT
# ==============================================================================
# Este script fornece uma interface interativa no terminal para gerenciar
# o ciclo de vida das aplicações Streamlit do projeto.
#
# Funcionalidades principais:
# 1. Menu de Ações: Escolha entre 'Reiniciar' ou 'Parar' os serviços.
# 2. Seleção de Escopo: Aplique a ação a um projeto específico 
#    (Painel de Observabilidade ou Painel de Analytics) ou a ambos simultaneamente.
# 3. Gestão de Processos: Identifica e encerra os processos (PIDs) exatos 
#    com base no caminho do arquivo, evitando derrubar outros serviços do servidor.
# 4. Reinicialização Inteligente: Ao escolher 'Reiniciar', o script derruba 
#    apenas o painel selecionado e aciona automaticamente o 'run_streamlit.sh' 
#    para subi-lo novamente com as configurações corretas de porta e logs.
# ==============================================================================

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "========================================="
echo "🛠️  Gerenciador de Painéis Streamlit"
echo "========================================="
echo "O que você deseja fazer?"
echo "1) Reiniciar"
echo "2) Parar"
read -p "Escolha uma opção (1 ou 2): " ACTION

if [[ "$ACTION" != "1" && "$ACTION" != "2" ]]; then
  echo "❌ Opção inválida."
  exit 1
fi

echo "-----------------------------------------"
echo "Qual projeto?"
echo "1) Painel de Observabilidade"
echo "2) Painel de Analytics"
echo "3) Ambos"
read -p "Escolha uma opção (1, 2 ou 3): " PROJECT

APP_OBS="streamlit/observability_hub.py"
APP_ANA="streamlit/analytics_hub.py"

APPS_TO_PROCESS=()

case $PROJECT in
  1) APPS_TO_PROCESS=("$APP_OBS") ;;
  2) APPS_TO_PROCESS=("$APP_ANA") ;;
  3) APPS_TO_PROCESS=("$APP_OBS" "$APP_ANA") ;;
  *) echo "❌ Opção inválida."; exit 1 ;;
esac

echo "-----------------------------------------"

for APP in "${APPS_TO_PROCESS[@]}"; do
  PROCESS_PATTERN="streamlit run $APP"
  APP_NAME=$(basename "$APP" .py)
  
  PID=$(ps aux | grep "$PROCESS_PATTERN" | grep -v grep | awk '{print $2}')
  
  if [ -z "$PID" ]; then
    echo "⚠️  $APP_NAME já está parado (nenhum processo encontrado)."
  else
    echo "🛑 Parando $APP_NAME (PID: $PID)..."
    kill -9 "$PID"
    echo "✅ $APP_NAME encerrado com sucesso."
  fi
done

if [ "$ACTION" == "1" ]; then
  echo "-----------------------------------------"
  echo "🔄 Iniciando rotina de reinicialização..."
  
  START_SCRIPT="$BIN_DIR/run_streamlit.sh" 
  
  if [ -f "$START_SCRIPT" ]; then
    bash "$START_SCRIPT"
  else
    echo "⚠️  Script de inicialização ($START_SCRIPT) não encontrado."
    echo "Por favor, inicie as aplicações manualmente."
  fi
fi

echo "========================================="
echo "🎉 Operação finalizada!"