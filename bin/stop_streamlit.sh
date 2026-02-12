#!/usr/bin/env bash
#chmod +x bin/stop_streamlit.sh

PROCESS_PATTERN="streamlit run streamlit/observability_hub.py"

PID=$(ps aux | grep "$PROCESS_PATTERN" | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
  echo "❌ Streamlit não está rodando (padrão: $PROCESS_PATTERN)"
else
  echo "🛑 Parando Streamlit (PID $PID)..."
  kill -9 "$PID"
  echo "✅ Streamlit encerrado com sucesso."
fi