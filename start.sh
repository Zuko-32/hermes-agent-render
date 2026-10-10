#!/usr/bin/env sh
set -e

# Variables por defecto si no están definidas
: "${PORT:=10000}"
: "${REMOTE_MCP_WS:=ws://89.6.129.67:3000}"

# Exportar para Node si tu app las lee desde process.env
export PORT
export REMOTE_MCP_WS

# Ejecutar el proxy en primer plano (no en background)
exec node /opt/app/ws-to-sse-proxy.js
