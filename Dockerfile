
FROM node:20-alpine
WORKDIR /opt/app

# Copiar package.json primero para cache de dependencias
COPY package*.json ./
RUN if [ -f package.json ]; then npm install --production; fi

# Copiar el resto de archivos
COPY . .

# Asegurar permisos
RUN chmod +x /opt/app/start.sh

ENV PORT=10000
EXPOSE 10000

# Ejecutar start.sh (que a su vez ejecuta node ws-to-sse-proxy.js)
CMD ["/opt/app/start.sh"]

