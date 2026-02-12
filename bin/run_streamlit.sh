#!/usr/bin/env bash
#chmod +x bin/run_streamlit.sh

set -e

echo "🚀 Iniciando Streamlit..."

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_DIR="$( dirname "$BIN_DIR" )"

STREAMLIT_APP="streamlit/observability_hub.py"
VENV_PATH="$APP_DIR/.venv"
PORT=8501

mkdir -p "$APP_DIR/bin/reports/"

cd "$APP_DIR"

if [ -d "$VENV_PATH" ]; then
  echo "🐍 Ativando virtualenv em $VENV_PATH"
  source "$VENV_PATH/bin/activate"
else
  echo "⚠️ Virtualenv não encontrado em $VENV_PATH. Tentando rodar com python global..."
fi

nohup streamlit run "$STREAMLIT_APP" \
  --server.port "$PORT" \
  --server.address 0.0.0.0 \
  > "$APP_DIR/bin/reports/streamlit.log" 2>&1 &

echo "✅ Streamlit rodando na porta $PORT"
echo "📝 Logs em: /bin/reports/streamlit.log"