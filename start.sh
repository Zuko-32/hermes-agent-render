#!/usr/bin/env sh
set -e
: "${PORT:=10000}"
: "${REMOTE_MCP_WS:=ws://89.6.129.67:3000}"
export PORT
export REMOTE_MCP_WS
exec node /opt/app/ws-to-sse-proxy.js
