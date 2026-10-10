#!/bin/sh
set -e

# Lanzar proxy SSE en background
node /opt/app/ws-to-sse-proxy.js &

# Espera corta opcional para asegurar que el proxy arranque
sleep 1

# Arrancar Hermes (ajusta el comando si tu entrypoint es distinto)
# Reemplaza la línea siguiente por el comando real que inicia Hermes en tu imagen
exec node /opt/app/hermes-entrypoint.js
