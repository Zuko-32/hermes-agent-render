# ==============================================================
# Hermes Agent + On-Server Web Chat (chat.html) for Render.com
# ==============================================================
FROM nousresearch/hermes-agent:latest

USER root

# Create directory structure and set open permissions for data
RUN mkdir -p /opt/hermes/web /opt/hermes/deploy /opt/hermes/docs /opt/data && \
    chmod -R 777 /opt/data

# Ensure Hermes Web Dashboard + PTY terminal dependencies are installed
RUN pip install --no-cache-dir "fastapi>=0.100" "uvicorn[standard]" "websockets" "ptyprocess" "httpx" || true

# Copy custom web chat, presentation, docs, and server proxy
COPY web/chat.html /opt/hermes/web/chat.html
COPY web/chat_web.html /opt/hermes/web/chat_web.html
COPY web/presentation.html /opt/hermes/web/presentation.html
COPY docs/index.html /opt/hermes/docs/index.html
COPY deploy/server.py /opt/hermes/deploy/server.py
COPY deploy/start.sh /opt/hermes/deploy/start.sh

RUN chmod +x /opt/hermes/deploy/start.sh

# Expose Render default port
EXPOSE 10000

# Start Hermes gateway + web proxy
CMD ["/opt/hermes/deploy/start.sh"]
