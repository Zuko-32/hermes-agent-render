# Master Manual: 24/7 Free Sovereign AI Server with Hermes Agent, Render & OpenRouter

> **Goal:** Run your personal, persistent Artificial Intelligence server in the cloud 24 hours a day **100% free of charge**, eliminating reliance on paid monthly subscriptions (ChatGPT Plus, Claude Pro, Gemini Advanced).
>
> **Stack:**
> 1. **OpenRouter**: Access state-of-the-art AI models at $0.00 cost (`:free` tier).
> 2. **Render.com**: Host your private containerized server 24/7 on the Free Web Service tier.
> 3. **Hermes Agent** (Nous Research): Persistent memory, self-evolving skills, and OpenAI-compatible API gateway.
> 4. **On-Server Web Chat (`chat.html`)**: Instant browser access directly on your domain without installing anything.
> 5. **Hermes Web Dashboard (`/dashboard`)**: Full visual administration and PTY web terminal.
> 6. **Telegram Bot** (optional): Chat with your agent on mobile or desktop via standard chat messaging.

---

### 🚀 Live Interactive Portals on Render Server
- 📖 **Interactive Master HTML Documentation**: [hermes-agent-render-a9ab.onrender.com/docs](https://hermes-agent-render-a9ab.onrender.com/docs)
- 📽 **Interactive Slide Deck Presentation**: [hermes-agent-render-a9ab.onrender.com/presentation](https://hermes-agent-render-a9ab.onrender.com/presentation)
- 💬 **Live Swiss Modernist Web Chat**: [hermes-agent-render-a9ab.onrender.com](https://hermes-agent-render-a9ab.onrender.com)
- 🎛 **Official Hermes Web Dashboard**: [hermes-agent-render-a9ab.onrender.com/dashboard](https://hermes-agent-render-a9ab.onrender.com/dashboard)

---

## 🌐 Language Index / Índice de Idiomas
1. [🇬🇧 English Manual](#-english-manual)
2. [🇪🇸 Manual en Español](#-manual-en-español)

---

# 🇬🇧 English Manual

## Table of Contents
1. [Architecture Overview](#1-architecture-overview)
2. [Prerequisites](#2-prerequisites)
3. [Step 1: Get Your Free OpenRouter Key](#step-1-get-your-free-openrouter-key)
4. [Step 2: Set Up Telegram Bot (Optional)](#step-2-set-up-telegram-bot-optional)
5. [Step 3: Deploy the Server on Render.com](#step-3-deploy-the-server-on-rendercom)
6. [Step 4: Using the On-Server Web Chat (`chat.html`)](#step-4-using-the-on-server-web-chat-chathtml)
7. [Step 5: Alternative Web Clients (`chat_web.html` & NextChat)](#step-5-alternative-web-clients-chat_webhtml--nextchat)
8. [Step 6: Hermes Web Dashboard (`/dashboard`)](#step-6-hermes-web-dashboard-dashboard)
9. [Free Models Catalog (`:free`)](#free-models-catalog-free)
10. [Keeping Your Free Server Awake 24/7](#keeping-your-free-server-awake-247)
11. [Troubleshooting & FAQ](#troubleshooting--faq)

---

### 1. Architecture Overview

```
+-------------------------------------------------------------+
|   Your Client Device                                        |
|   (Browser Chat / Web Dashboard / Desktop App / Telegram)   |
+------------------------------+------------------------------+
                               |  HTTPS & WebSockets
                               v
+------------------------------+------------------------------+
|   Render.com (Free Web Service - Port :10000)               |
|   - Reverse Proxy & Tunnel (deploy/server.py)               |
|     --> Serves Swiss Chat UI at '/'                         |
|     --> Proxies '/dashboard' & SPA to Dashboard (:9119)     |
|     --> WS Raw TCP Tunnel for '/api/ws' & '/api/pty'        |
|     --> Proxies '/v1/*' to Gateway (:8642)                  |
|   - Official Hermes Web Dashboard (:9119)                   |
|   - Hermes Agent Gateway & Runtime (:8642)                  |
+------------------------------+------------------------------+
                               |  Inference API Calls
                               v
+------------------------------+------------------------------+
|   OpenRouter.ai (:free models)                              |
|   - Llama 3.3 70B, Gemini 2.0 Flash Lite, DeepSeek R1, Qwen |
+-------------------------------------------------------------+
```

---

### 2. Prerequisites
- A web browser (Chrome, Edge, Safari, Firefox).
- A free email account or Google account.
- No coding or server administration skills required.

---

### Step 1: Get Your Free OpenRouter Key
1. Go to **[https://openrouter.ai/](https://openrouter.ai/)**.
2. Click **Sign In** and authenticate using Google or email.
3. Open the API Keys panel: **[https://openrouter.ai/keys](https://openrouter.ai/keys)**.
4. Click **Create Key**:
   - **Key Name**: `Hermes Free`
   - **Credit Limit**: Leave blank (unlimited for free models).
5. Click **Create** and copy your secret key starting with `sk-or-v1-...`.
> *Note: Your account balance will remain $0.00. Free models ending with `:free` do not consume credits or require a credit card.*

---

### Step 2: Set Up Telegram Bot (Optional)
If you want to chat from your mobile phone:
1. Open Telegram and search for **`@BotFather`** (verified badge).
2. Send `/newbot`.
3. Provide a display name (e.g. `My Hermes Assistant`) and a unique username ending in `bot` (e.g. `my_hermes_2026_bot`).
4. Save the **HTTP API Token** provided by BotFather.
5. In Telegram search for **`@userinfobot`**, click Start, and note your numeric **Id**. This prevents anyone else from accessing your bot.

---

### Step 3: Deploy the Server on Render.com

#### Option A: Deploy via GitHub (Recommended — Includes On-Server `chat.html`)
1. Push or fork this repository to your GitHub account (or use `https://github.com/thurtado1993/hermes-agent-render`).
2. Sign in to **[https://render.com/](https://render.com/)**.
3. In the Dashboard, click **+ New** ➔ **Web Service**.
4. Select your connected GitHub repository.
5. Configure the service:
   - **Name**: `hermes-agent-free`
   - **Region**: Select Frankfurt (EU) or Oregon/Ohio (US).
   - **Branch**: `main`
   - **Runtime / Environment**: `Docker` (Render automatically detects the root `./Dockerfile`).
   - **Instance Type**: **Free ($0/month)**.

> [!NOTE]
> Render looks for `./Dockerfile` at the root of the repository. We provide `Dockerfile` right at the root so zero manual path configuration is needed.

#### Option B: Deploy with Render Blueprint (`render.yaml`)
1. In Render Dashboard, click **+ New** ➔ **Blueprint**.
2. Connect this repository. Render will automatically read `render.yaml` from the root and configure all variables and ports automatically.

#### Option C: Deploy Pre-built Image (Quick No-Code Setup without custom chat.html)
1. In Render, select **"Existing Image"**.
2. Enter: `docker.io/nousresearch/hermes-agent:latest`.
3. Select the **Free** instance type.

#### Environment Variables (Both options)
Add the following keys under the **Environment Variables** section:

| Variable | Recommended Value | Explanation |
| :--- | :--- | :--- |
| `OPENROUTER_API_KEY` | *(Your `sk-or-v1-...` key)* | Connects agent to OpenRouter |
| `MODEL_NAME` | `meta-llama/llama-3.3-70b-instruct:free` | Default high-capability free model |
| `PORT` | `10000` | Port expected by Render router |
| `API_SERVER_ENABLED` | `true` | Enables OpenAI-compatible API |
| `API_SERVER_PORT` | `10000` (or `8642` with Dockerfile) | Gateway server port |
| `API_SERVER_KEY` | *(Your secret password)* | Protects access to the API |
| `TELEGRAM_BOT_TOKEN` | *(From @BotFather)* | Enables mobile Telegram bot |
| `TELEGRAM_ALLOWED_USERS`| *(Your numeric Telegram ID)* | Restricts bot to your account only |
| `HERMES_DASHBOARD_BASIC_AUTH_USERNAME` | *(Optional username, e.g. admin)* | Enables HTTP Basic Auth on dashboard |
| `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD` | *(Optional password)* | Dashboard HTTP Basic Auth password |

Click **Create Web Service**. After 2–3 minutes, the status badge will turn green (**Live**).

---

### Step 4: Using the On-Server Web Chat (`chat.html`)
If deployed using our repository's `Dockerfile`:
1. Open your web browser on any device (laptop, smartphone, iPad).
2. Navigate directly to your Render public URL:
   ```text
   https://hermes-agent-free.onrender.com
   ```
3. The on-server web chat interface will load instantly.
4. Enter your `API_SERVER_KEY` once when prompted.
5. You can now chat directly with your Hermes Agent with **zero configuration, zero CORS issues, and no external dependencies**!

---

### Step 5: Alternative Web Clients (`chat_web.html` & NextChat)

#### 1. Standalone File (`web/chat_web.html`)
- Double click `web/chat_web.html` on your computer.
- In the sidebar, set your Render URL (`https://your-service.onrender.com`) and your `API_SERVER_KEY`.
- Click **Save Settings** and start chatting.

#### 2. NextChat Web
- Visit **[https://app.nextchat.dev/](https://app.nextchat.dev/)**.
- Go to Settings ➔ Provider: **Custom / OpenAI**.
- Endpoint: `https://your-service.onrender.com/v1`.
- API Key: Your `API_SERVER_KEY`.

---

### Step 6: Hermes Web Dashboard (`/dashboard`)

For advanced users who want full visual control over their Hermes Agent configuration, tools, and background processes:

#### 1. Accessing the Dashboard
- **Direct Link**: Visit `https://your-service.onrender.com/dashboard` in any browser.
- **Shortcut Button**: Click the `[ 🎛 DASHBOARD ]` button in the header of `chat.html` or `chat_web.html`.
- **Drawer Links**: Open the `[ SETTINGS ]` drawer in `chat.html` to jump directly into specific panels (Config, Skills, MCP, Logs, Cron, Analytics).

#### 2. Features & Management Panels
The official Hermes Web Dashboard runs on internal port `9119` and is routed seamlessly by the built-in reverse proxy with full WebSocket and PTY terminal support:
- **Config Editor (`/config`)**: Visually inspect and edit your active `config.yaml` without opening a terminal. Change providers, toggle tools, adjust context parameters, and update system prompts.
- **Skills Manager (`/skills`)**: Browse installed skills, inspect user-created abilities, enable/disable tools, and write custom skill manifests.
- **MCP Servers (`/mcp`)**: Add, test, and manage external Model Context Protocol integrations (filesystem, database, web tools).
- **Scheduled Jobs & Cron (`/cron`)**: Schedule recurring automated agent actions, reminders, and self-directed routines.
- **Live Logs & Stream (`/logs`)**: Watch real-time agent execution logs, tool call arguments, outputs, and stack traces.
- **Interactive Terminal PTY (`/terminal` via `/api/pty`)**: Direct shell access inside your container right from the browser via xterm.js over WebSockets.
- **Sessions & Chat Archive (`/sessions`)**: Inspect all past agent conversations, memory dumps, and message history.
- **Token Analytics & Usage (`/analytics`)**: Track prompt and completion tokens, estimated costs, and model performance.
- **Webhooks & Channel Hub**: Configure Discord, Slack, and custom webhooks for event notifications.

#### 3. Connecting Hermes Desktop App Remotely
If you use the native [Hermes Desktop](https://hermes-agent.nousresearch.com/docs/user-guide/features/desktop) application on macOS, Windows, or Linux:
1. Open Hermes Desktop ➔ Settings ➔ **Connection**.
2. Select **Remote Server**.
3. Set Server URL: `https://your-service.onrender.com`.
4. Enter your `API_SERVER_KEY`.
5. The desktop app connects seamlessly through the reverse proxy's WebSocket tunnel (`/api/ws`).

---

### Free Models Catalog (`:free`)

| Model Identifier | Primary Focus | Best Use Case |
| :--- | :--- | :--- |
| `meta-llama/llama-3.3-70b-instruct:free` | **All-Rounder** | 70B parameters, exceptional Spanish and English reasoning, creative writing. |
| `google/gemini-2.0-flash-lite:free` | **Speed & Context** | Near-zero latency, large context window for big documents. |
| `deepseek/deepseek-r1:free` | **Deep Reasoning** | Chain-of-thought logic, math, riddles, and scientific deduction. |
| `qwen/qwen-2.5-coder-32b-instruct:free` | **Coding Specialist** | Python, JavaScript, bug diagnosis, architecture design. |
| `openrouter/free` | **Smart Router** | Automatically routes prompts to whichever free model is currently healthiest. |

---

### Keeping Your Free Server Awake 24/7
Render's free tier idles after 15 minutes of inactivity. To eliminate cold starts:
1. Copy your Render URL (`https://your-service.onrender.com`).
2. Go to **[https://cron-job.org/](https://cron-job.org/)** (free).
3. Create a cronjob making a simple HTTP GET request to your URL every **10 minutes**.
4. Your server will stay active 24 hours a day with zero delays.

---

### Troubleshooting & FAQ
- **Why did my first message take 40 seconds?** The free server was asleep. Subsequent messages respond in 1–2 seconds. Use the keep-alive tip above.
- **Telegram bot does not answer?** Verify that `TELEGRAM_ALLOWED_USERS` matches your exact ID from `@userinfobot`.
- **Can anyone else access my server?** No. Web endpoints require your `API_SERVER_KEY`, and Telegram strictly enforces your user ID.

---
---

# 🇪🇸 Manual en Español

## Índice de Contenidos
1. [Visión General de la Arquitectura](#1-visión-general-de-la-arquitectura)
2. [Requisitos Previos](#2-requisitos-previos-1)
3. [Paso 1: Obtener tu Clave Gratuita de OpenRouter](#paso-1-obtener-tu-clave-gratuita-de-openrouter-1)
4. [Paso 2: Configurar el Bot de Telegram (Opcional)](#paso-2-configurar-el-bot-de-telegram-opcional)
5. [Paso 3: Desplegar el Servidor en Render.com](#paso-3-desplegar-el-servidor-en-rendercom)
6. [Paso 4: Usar el Chat Web en el Servidor (`chat.html`)](#paso-4-usar-el-chat-web-en-el-servidor-chathtml)
7. [Paso 5: Clientes Web Alternativos (`chat_web.html` y NextChat)](#paso-5-clientes-web-alternativos-chat_webhtml-y-nextchat)
8. [Paso 6: Panel de Control Web de Hermes (`/dashboard`)](#paso-6-panel-de-control-web-de-hermes-dashboard)
9. [Catálogo de Modelos Gratuitos (`:free`)](#catálogo-de-modelos-gratuitos-free)
10. [Mantener el Servidor Despierto 24/7](#mantener-el-servidor-despierto-247)
11. [Preguntas Frecuentes y Resolución de Problemas](#preguntas-frecuentes-y-resolución-de-problemas)

---

### 1. Visión General de la Arquitectura

* **Hermes Agent**: Cerebro autónomo con memoria persistente desarrollado por Nous Research.
* **Hermes Web Dashboard**: Panel de control oficial para administrar habilidades, MCP, configuración, cron jobs y logs.
* **OpenRouter**: Acceso a modelos potentes con coste cero (`:free`).
* **Render.com**: Servidor en la nube gratuito 24/7 sin tarjeta bancaria.
* **chat.html**: Interfaz web integrada en tu propio dominio de Render.
* **Telegram**: Acceso desde el móvil estés donde estés.

---

### 2. Requisitos Previos
* Un navegador web moderno (Chrome, Edge, Firefox, Safari).
* Una cuenta de correo o Google.
* Cero conocimientos de programación o servidores.

---

### Paso 1: Obtener tu Clave Gratuita de OpenRouter
1. Entra en **[https://openrouter.ai/](https://openrouter.ai/)** y pulsa **Sign In**.
2. Ve a la sección de claves: **[https://openrouter.ai/keys](https://openrouter.ai/keys)**.
3. Haz clic en **Create Key**:
   * **Nombre**: `Hermes Gratis`
   * **Límite de crédito**: Déjalo en blanco.
4. Pulsa **Create** y copia la clave que empieza por `sk-or-v1-...`.

---

### Paso 2: Configurar el Bot de Telegram (Opcional)
1. En Telegram, busca **`@BotFather`** y envía `/newbot`.
2. Dale un nombre visible y un nombre de usuario que termine en `bot`.
3. Guarda el **HTTP API Token** proporcionado.
4. Busca **`@userinfobot`**, pulsa Iniciar y copia tu número de **Id** para proteger el acceso.

---

### Paso 3: Desplegar el Servidor en Render.com

#### Opción A: Despliegue mediante GitHub (Recomendado — Incluye chat web en el servidor)
1. Sube o haz fork de este repositorio a tu cuenta de GitHub (o usa `https://github.com/thurtado1993/hermes-agent-render`).
2. Inicia sesión en **[https://render.com/](https://render.com/)**.
3. En el panel principal, haz clic en **+ New** ➔ **Web Service**.
4. Selecciona tu repositorio de GitHub conectado.
5. Configura el servicio:
   * **Name**: `hermes-agent-free`
   * **Region**: Selecciona Frankfurt (Europa) o Oregon/Ohio (EE. UU.).
   * **Branch**: `main`
   * **Runtime / Environment**: `Docker` (Render detecta automáticamente el `Dockerfile` ubicado en la raíz del repositorio).
   * **Instance Type**: **Free ($0/month)**.

> [!NOTE]
> Render busca por defecto el archivo `Dockerfile` en la raíz del repositorio. Este repositorio incluye `Dockerfile` directamente en la raíz, por lo que no es necesario realizar configuraciones manuales de rutas.

#### Opción B: Despliegue con Blueprint (`render.yaml`)
1. En el panel de Render, pulsa en **+ New** ➔ **Blueprint**.
2. Conecta este repositorio. Render leerá automáticamente el archivo `render.yaml` de la raíz y configurará los servicios y variables.

#### Opción C: Despliegue con Imagen Precompilada (Sin chat.html integrado)
1. En Render, selecciona **"Existing Image"**.
2. Introduce: `docker.io/nousresearch/hermes-agent:latest`.
3. Elige el plan **Free**.

#### Variables de Entorno (Environment Variables)
Añade las siguientes claves en la sección **Environment Variables**:

| Variable | Valor Recomendado | Explicación |
| :--- | :--- | :--- |
| `OPENROUTER_API_KEY` | *(Tu clave `sk-or-v1-...`)* | Conecta el agente con OpenRouter |
| `MODEL_NAME` | `meta-llama/llama-3.3-70b-instruct:free` | Modelo gratuito potente por defecto |
| `PORT` | `10000` | Puerto HTTP esperado por el router de Render |
| `API_SERVER_KEY` | *(Tu contraseña secreta)* | Protege el acceso al servidor y chat |
| `TELEGRAM_BOT_TOKEN` | *(Opcional, de @BotFather)* | Habilita el bot móvil de Telegram |
| `TELEGRAM_ALLOWED_USERS`| *(Opcional, ID numérico)* | Restringe el bot únicamente a tu usuario |
| `HERMES_DASHBOARD_BASIC_AUTH_USERNAME` | *(Opcional, ej. admin)* | Usuario para autenticación básica en dashboard |
| `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD` | *(Opcional)* | Contraseña para autenticación en dashboard |

Haz clic en **Create Web Service**. Espera 2–3 minutos hasta ver la etiqueta verde **Live**.

---

### Paso 4: Usar el Chat Web en el Servidor (`chat.html`)
Si has desplegado el proyecto con el `Dockerfile` incluido:
1. Abre tu navegador en cualquier dispositivo (ordenador, móvil o tablet).
2. Entra directamente a la URL de tu Render:
   ```text
   https://tu-servicio.onrender.com
   ```
3. La interfaz web cargará al instante directamente desde tu servidor.
4. Introduce tu contraseña `API_SERVER_KEY` una sola vez.
5. ¡Empieza a chatear sin instalar nada, con conexión directa y sin bloqueos de CORS!

---

### Paso 5: Clientes Web Alternativos (`chat_web.html` y NextChat)

#### 1. Archivo local (`web/chat_web.html`)
Haz doble clic sobre `web/chat_web.html` en tu ordenador, introduce la URL de Render y tu clave API, y disfruta de un chat privado en local.

#### 2. NextChat Web
Entra en **[https://app.nextchat.dev/](https://app.nextchat.dev/)**, ve a Ajustes ➔ Custom OpenAI, y pon tu URL de Render (`https://tu-servicio.onrender.com/v1`) con tu contraseña.

---

### Paso 6: Panel de Control Web de Hermes (`/dashboard`)

Para usuarios avanzados que deseen un control visual total sobre la configuración de Hermes, herramientas, extensiones y procesos en segundo plano:

#### 1. Cómo Acceder al Dashboard
- **Enlace directo**: Abre en cualquier navegador `https://tu-servicio.onrender.com/dashboard`.
- **Botón directo**: Pulsa el botón `[ 🎛 DASHBOARD ]` en la barra superior de `chat.html` o `chat_web.html`.
- **Accesos desde Ajustes**: Abre el panel `[ SETTINGS ]` en `chat.html` para acceder con un clic a Configuración, Habilidades, MCP, Registros o Tareas Cron.

#### 2. Módulos y Paneles de Gestión Disponibles
El Dashboard oficial de Hermes funciona internamente en el puerto `9119` y es expuesto fluidamente por el servidor proxy inverso con soporte completo de WebSockets y emulación de terminal PTY:
- **Editor de Configuración (`/config`)**: Inspecciona y edita visualmente tu `config.yaml` sin tocar la consola. Cambia proveedores, activa o desactiva herramientas, amplía la ventana de contexto o modifica los prompts de sistema.
- **Gestor de Habilidades (`/skills`)**: Explora las habilidades instaladas, visualiza las destrezas creadas por el agente, habilita/deshabilita funciones y programa nuevas skills.
- **Servidores MCP (`/mcp`)**: Añade, prueba y monitoriza integraciones del Model Context Protocol (bases de datos, sistema de ficheros, APIs externas).
- **Tareas Programadas / Cron (`/cron`)**: Programa acciones recurrentes, recordatorios y rutinas automatizadas para que el agente trabaje de forma autónoma.
- **Registros en Tiempo Real (`/logs`)**: Visualiza en vivo la ejecución de llamadas a herramientas, argumentos, salidas y trazas de depuración.
- **Terminal Web Integrada (`/terminal` vía `/api/pty`)**: Accede a una consola interactiva dentro del contenedor directamente desde el navegador con xterm.js sobre WebSocket.
- **Historial de Sesiones (`/sessions`)**: Consulta conversaciones anteriores, volcado de memoria y estado del contexto.
- **Métricas y Consumo de Tokens (`/analytics`)**: Supervisa tokens de entrada y salida, estimación de costes y rendimiento.
- **Canales y Webhooks**: Configura alertas hacia Discord, Slack o webhooks personalizados.

#### 3. Conectar la App Nativa Hermes Desktop
Si utilizas la aplicación de escritorio [Hermes Desktop](https://hermes-agent.nousresearch.com/docs/user-guide/features/desktop) en Windows, macOS o Linux:
1. Abre Hermes Desktop ➔ Ajustes ➔ **Connection**.
2. Selecciona **Remote Server**.
3. Indica la URL del servidor: `https://tu-servicio.onrender.com`.
4. Introduce tu `API_SERVER_KEY`.
5. La aplicación de escritorio se conectará a través del túnel de WebSocket (`/api/ws`) integrado en Render.

---

### Catálogo de Modelos Gratuitos (`:free`)

| Modelo | Especialidad | Ventajas |
| :--- | :--- | :--- |
| `meta-llama/llama-3.3-70b-instruct:free` | **Todoterreno** | 70B parámetros, redacción y razonamiento de primer nivel. |
| `google/gemini-2.0-flash-lite:free` | **Velocidad** | Respuestas inmediatas y gran ventana de contexto. |
| `deepseek/deepseek-r1:free` | **Lógica** | Razonamiento reflexivo paso a paso para matemáticas y ciencia. |
| `qwen/qwen-2.5-coder-32b-instruct:free` | **Programación** | Análisis y generación de código de alta precisión. |
| `openrouter/free` | **Auto Router** | Enrutador automático al modelo libre más rápido disponible. |

---

### Mantener el Servidor Despierto 24/7
Copia tu URL de Render y crea una tarea gratuita en **[cron-job.org](https://cron-job.org)** que haga una petición HTTP simple cada **10 minutos**. ¡Tu servidor responderá al instante las 24 horas del día!
