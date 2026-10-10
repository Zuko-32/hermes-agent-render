# Imagen base ligera con Node 20
FROM node:20-alpine

# Directorio de trabajo dentro del contenedor
WORKDIR /opt/app

# Copiar package.json y package-lock.json (si existe) e instalar dependencias
COPY package*.json ./
RUN npm install --production

# Copiar el resto de archivos de la app al contenedor
COPY . .

# Asegurar que el script de arranque sea ejecutable
COPY ws-to-sse-proxy.js /opt/app/ws-to-sse-proxy.js
COPY start.sh /opt/app/start.sh
RUN chmod +x /opt/app/start.sh

# Puerto que expondrá la app (Render usará la variable PORT)
ENV PORT=10000
EXPOSE 10000

# Comando que arranca el contenedor (usa tu start.sh)
CMD ["/opt/app/start.sh"]
