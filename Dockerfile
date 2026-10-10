# --- base image y pasos previos que ya tengas ---
FROM node:20-alpine

WORKDIR /opt/app

# Copiar app existente
COPY package*.json ./
RUN npm install --production

COPY . .

# Copiar proxy y script de arranque
COPY ws-to-sse-proxy.js /opt/app/ws-to-sse-proxy.js
COPY start.sh /opt/app/start.sh
RUN chmod +x /opt/app/start.sh

ENV PORT=10000
EXPOSE 10000

# Comando de arranque que lanza proxy y Hermes
CMD ["/opt/app/start.sh"]
