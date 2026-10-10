#!/bin/bash
set -e

echo "=========================================================="
echo "      HERMES AGENT BOOT SEQUENCE - RENDER DEPLOYMENT      "
echo "=========================================================="

export HERMES_HOME="${HERMES_HOME:-/opt/data}"
export API_SERVER_PORT=8642
export API_SERVER_HOST=0.0.0.0
export API_SERVER_ENABLED=true
export API_SERVER_KEY="${API_SERVER_KEY:-secret_hermes_2026_key}"
export OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-}"
export MODEL_NAME="${MODEL_NAME:-openrouter/free}"
export HERMES_GATEWAY_PORT=8642

echo "[*] Setting up workspace directories in ${HERMES_HOME}..."
mkdir -p "${HERMES_HOME}" "${HERMES_HOME}/.hermes" "/root/.hermes" "/home/hermes/.hermes" 2>/dev/null || true

# Generate config.yaml across all search locations
cat <<EOF > "${HERMES_HOME}/config.yaml"
model:
  provider: openrouter
  name: "${MODEL_NAME}"
gateway:
  api_server:
    enabled: true
    port: 8642
    host: 0.0.0.0
    key: "${API_SERVER_KEY}"
platforms:
  api_server:
    enabled: true
    port: 8642
    host: 0.0.0.0
    key: "${API_SERVER_KEY}"
EOF

cp "${HERMES_HOME}/config.yaml" "${HERMES_HOME}/.hermes/config.yaml" 2>/dev/null || true
cp "${HERMES_HOME}/config.yaml" "/root/.hermes/config.yaml" 2>/dev/null || true
cp "${HERMES_HOME}/config.yaml" "/home/hermes/.hermes/config.yaml" 2>/dev/null || true

# Generate .env across all search locations
cat <<EOF > "${HERMES_HOME}/.env"
API_SERVER_ENABLED=true
API_SERVER_PORT=8642
API_SERVER_HOST=0.0.0.0
API_SERVER_KEY="${API_SERVER_KEY}"
OPENROUTER_API_KEY="${OPENROUTER_API_KEY}"
OPENAI_API_KEY="${OPENAI_API_KEY:-}"
MODEL_NAME="${MODEL_NAME}"
HERMES_HOME="${HERMES_HOME}"
EOF

cp "${HERMES_HOME}/.env" "${HERMES_HOME}/.hermes/.env" 2>/dev/null || true
cp "${HERMES_HOME}/.env" "/root/.hermes/.env" 2>/dev/null || true
cp "${HERMES_HOME}/.env" "/home/hermes/.hermes/.env" 2>/dev/null || true

chmod -R 777 "${HERMES_HOME}" 2>/dev/null || true

# Apply config through hermes CLI
echo "[*] Configuring Hermes runtime platform..."
hermes config set API_SERVER_ENABLED true 2>/dev/null || true
hermes config set API_SERVER_PORT 8642 2>/dev/null || true
hermes config set API_SERVER_HOST 0.0.0.0 2>/dev/null || true
hermes config set API_SERVER_KEY "${API_SERVER_KEY}" 2>/dev/null || true
hermes config set gateway.api_server.enabled true 2>/dev/null || true
hermes config set gateway.api_server.port 8642 2>/dev/null || true
hermes config set gateway.api_server.host 0.0.0.0 2>/dev/null || true
hermes config set gateway.api_server.key "${API_SERVER_KEY}" 2>/dev/null || true
hermes config set platforms.api_server.enabled true 2>/dev/null || true

echo "[*] Starting Hermes Gateway in background (logging to /tmp/hermes-gateway.log)..."
(hermes gateway run > /tmp/hermes-gateway.log 2>&1) &
HERMES_PID=$!

echo "[*] Hermes PID: $HERMES_PID. Waiting for API Server (port 8642) to bind..."
GATEWAY_READY=false
for i in $(seq 1 15); do
  if python3 -c "import socket; s = socket.socket(); s.connect(('127.0.0.1', 8642)); s.close()" 2>/dev/null; then
    echo "[✓] Hermes API Server listening on 127.0.0.1:8642! (Ready in ${i}s)"
    GATEWAY_READY=true
    break
  fi
  sleep 1
done

if [ "$GATEWAY_READY" = false ]; then
  echo "[!] Notice: Gateway port 8642 not open after 15s. Checking startup logs:"
  head -n 25 /tmp/hermes-gateway.log 2>/dev/null || echo "No gateway logs yet."
  echo "[*] Web Proxy will use resilient direct upstream fallback for chat completions."
fi

# ==========================================================
# Start Official Hermes Web Dashboard (Port 9119)
# ==========================================================
echo "[*] Starting Hermes Web Dashboard on port 9119 (logging to /tmp/hermes-dashboard.log)..."
(hermes dashboard --host 127.0.0.1 --port 9119 --no-open > /tmp/hermes-dashboard.log 2>&1) &
DASHBOARD_PID=$!

echo "[*] Dashboard PID: $DASHBOARD_PID. Checking Dashboard (port 9119)..."
for i in $(seq 1 10); do
  if python3 -c "import socket; s = socket.socket(); s.connect(('127.0.0.1', 9119)); s.close()" 2>/dev/null; then
    echo "[✓] Hermes Web Dashboard listening on 127.0.0.1:9119! (Ready in ${i}s)"
    break
  fi
  sleep 1
done

echo "[*] Starting On-Server Web Chat & Unified Proxy on port ${PORT:-10000}..."
python3 /opt/hermes/deploy/server.py &
PROXY_PID=$!

trap "kill $HERMES_PID $DASHBOARD_PID $PROXY_PID 2>/dev/null || true" SIGINT SIGTERM
wait -n
