#!/usr/bin/env bash
#chmod +x bin/run_streamlit.sh
#
# ==============================================================================
# INICIALIZADOR DE PAINÉIS STREAMLIT
# ==============================================================================
# Este script é responsável por subir as aplicações Streamlit do projeto de
# forma automatizada, iterativa e segura, rodando em segundo plano.
#
# Funcionalidades principais:
# 1. Preparação de Ambiente: Cria o diretório de logs e ativa automaticamente
#    o ambiente virtual Python (.venv), caso ele exista.
# 2. Execução Iterativa: Percorre uma lista de aplicativos mapeados com suas
#    respectivas portas (Observability na 8501 e Analytics na 8502).
# 3. Validação Anti-Conflito: Verifica ativamente se a porta já está ocupada
#    antes de tentar subir o app, ignorando a inicialização caso já esteja rodando.
# 4. Background e Logs Dinâmicos: Utiliza 'nohup' para manter os serviços ativos
#    após o fechamento do terminal e gera arquivos de log individuais
#    (ex: observability_hub.log) na pasta bin/reports/.
# ==============================================================================

set -e

echo "🚀 Iniciando Apps Streamlit..."

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_DIR="$( dirname "$BIN_DIR" )"
VENV_PATH="$APP_DIR/.venv"

mkdir -p "$APP_DIR/bin/reports/"

cd "$APP_DIR"

if [ -d "$VENV_PATH" ]; then
  echo "🐍 Ativando virtualenv em $VENV_PATH"
  source "$VENV_PATH/bin/activate"
else
  echo "⚠️ Virtualenv não encontrado em $VENV_PATH. Tentando rodar com python global..."
fi

APPS=(
  "streamlit/observability_hub.py:8501"
  "streamlit/analytics_hub.py:8502"
)

for APP_INFO in "${APPS[@]}"; do
  APP_PATH="${APP_INFO%%:*}"
  PORT="${APP_INFO##*:}"
  
  APP_NAME=$(basename "$APP_PATH" .py)
  LOG_FILE="$APP_DIR/bin/reports/${APP_NAME}.log"

  echo "----------------------------------------"
  echo "🔍 Verificando $APP_PATH na porta $PORT..."


  if ss -tuln | grep -E -q ":$PORT\b"; then
    echo "⏭️  Porta $PORT já está em uso! Ignorando a inicialização de $APP_NAME."
  else
    echo "▶️  Iniciando $APP_NAME na porta $PORT..."
    
    nohup streamlit run "$APP_PATH" \
      --server.port "$PORT" \
      --server.address 0.0.0.0 \
      > "$LOG_FILE" 2>&1 &
    
    echo "✅ $APP_NAME inicializado na porta $PORT"
    echo "📝 Logs em: bin/reports/${APP_NAME}.log"
  fi
done

echo "----------------------------------------"
echo "🎉 Execução do script finalizada!"