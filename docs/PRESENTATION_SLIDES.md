---
marp: true
theme: default
paginate: true
header: "Hermes Agent + Render + OpenRouter Free Tier"
footer: "Zero-Cost Autonomous AI Server Guide"
style: |
  section {
    background-color: #090d16;
    color: #f8fafc;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  h1 { color: #38bdf8; }
  h2 { color: #818cf8; }
  a { color: #38bdf8; }
  code { background-color: #0f172a; color: #f43f5e; padding: 2px 6px; border-radius: 4px; }
  table { font-size: 0.85em; }
  th { background-color: #0f172a; color: #38bdf8; }
---

# Your Personal 24/7 AI Cloud Server
### Step-by-Step Beginner Masterclass
**Hermes Agent + Render.com + OpenRouter**

* Eliminate $20+/month subscriptions permanently
* 100% Free tier infrastructure & models (:free)
* Direct on-server web chat (`chat.html`) & Telegram mobile access

---

# Why This Project?

* **The Problem:** Subscriptions like ChatGPT Plus or Claude Pro cost $240+ annually.
* **The Solution:**
  * **Hermes Agent (Nous Research):** Persistent memory, tool calling, autonomous execution.
  * **OpenRouter:** Access cutting-edge models (Llama 3.3 70B, Gemini Flash) at $0.00 cost.
  * **Render.com:** Cloud hosting with 750 free monthly instance hours.
  * **On-Server Web Chat (`chat.html`):** Hosted directly on your Render domain.

---

# System Flow

```
[ Browser / Smartphone ]
       │ (chat.html or Telegram)
       ▼
[ Render Web Service ] ──────▶ Hermes Agent Gateway (:8642)
       │ (Inference requests)
       ▼
[ OpenRouter.ai ] ───────────▶ Free Models (:free)
```

* **Monthly Cost:** **$0.00**
* **Credit Card:** **Not required**
* **Maintenance:** **Zero**

---

# Step 1: OpenRouter API Key (2 min)

1. Navigate to **[openrouter.ai](https://openrouter.ai)** and click **Sign In**.
2. Visit **[openrouter.ai/keys](https://openrouter.ai/keys)**.
3. Click **Create Key**:
   * Name: `Hermes Free`
   * Credit limit: *Leave empty*
4. Copy your secret key starting with `sk-or-v1-...`.

> 💡 **Notice:** Your balance will remain $0.00. Free models ending with `:free` cost nothing.

---

# Step 2: Telegram Bot (Optional - 2 min)

1. Open Telegram and search for **`@BotFather`**.
2. Send `/newbot`.
3. Provide a display name and unique username ending in `bot`.
4. Copy the **HTTP API Token** from BotFather.
5. In Telegram, search for **`@userinfobot`**, click Start, and copy your numeric **Id**.

> 🔒 **Security:** Your agent will only obey commands from your verified user ID.

---

# Step 3: Deploy on Render.com

1. Sign up on **[render.com](https://render.com)**.
2. In Dashboard, click **+ New** ➔ **Web Service**.
3. Connect this GitHub repo (Render automatically detects the root `Dockerfile`) or pick **Existing Image**:
   ```text
   docker.io/nousresearch/hermes-agent:latest
   ```
4. Choose the **Free ($0/month)** instance plan.

---

# Step 3 (Cont.): Environment Variables

Add the following environment variables:

| Key | Value |
| :--- | :--- |
| `OPENROUTER_API_KEY` | *(Your `sk-or-v1-...` key)* |
| `MODEL_NAME` | `meta-llama/llama-3.3-70b-instruct:free` |
| `PORT` | `10000` |
| `API_SERVER_KEY` | *(Your custom server password)* |
| `TELEGRAM_BOT_TOKEN` | *(From @BotFather - optional)* |
| `TELEGRAM_ALLOWED_USERS` | *(Your numeric Telegram ID - optional)* |

Click **Create Web Service**. The status will turn green (**Live**) in ~2 minutes!

---

# Step 4: On-Server Web Chat (`chat.html`)

* Open your browser and go directly to your Render URL:
  ```text
  https://your-service.onrender.com
  ```
* Enter your `API_SERVER_KEY` once when prompted.
* **Benefits:**
  * Direct origin connection (relative `/v1/chat/completions` API calls).
  * Zero CORS issues.
  * Accessible from any laptop, smartphone, or tablet without installing anything.

---

# Standalone Client & Alternatives

* **Local File (`web/chat_web.html`):**
  Double click the included HTML file on your desktop. Enter your Render URL & key.
* **NextChat Web:**
  Visit [app.nextchat.dev](https://app.nextchat.dev). In Settings, select Custom OpenAI and point to `https://your-service.onrender.com/v1`.
* **Telegram Web:**
  Visit [web.telegram.org](https://web.telegram.org) to chat with your bot in any browser tab.

---

# Free Models Showcase (:free)

Switch models anytime by changing `MODEL_NAME` in Render:

| Model ID | Best For |
| :--- | :--- |
| `meta-llama/llama-3.3-70b-instruct:free` | **All-Rounder:** 70B params, outstanding reasoning. |
| `google/gemini-2.0-flash-lite:free` | **Speed:** Near-instant replies, massive context. |
| `deepseek/deepseek-r1:free` | **Reasoning:** Step-by-step thinking for math/logic. |
| `qwen/qwen-2.5-coder-32b-instruct:free` | **Code:** Architecture, debugging, and syntax. |
| `openrouter/free` | **Smart Router:** Picks the best active free model. |

---

# 24/7 Keep-Alive Pro Tip

* **Render Free Sleep:** Instances sleep after 15 min of inactivity.
* **How to keep it 100% active for free:**
  1. Copy your Render URL (`https://your-service.onrender.com`).
  2. Create a free account on [cron-job.org](https://cron-job.org).
  3. Set up an automated HTTP GET ping every **10 minutes**.
  4. Your server will stay permanently active with instant responses!

---

# Summary of Achievements

✅ **Zero Costs:** $0/mo permanently, no credit card required.
✅ **High Capability:** 70B parameter open-source intelligence.
✅ **Total Flexibility:** On-server web chat, standalone HTML, and Telegram bot.
✅ **Sovereignty:** Your private container, your keys, your memories.

🎉 **Congratulations! You are officially subscription-free!**

---
---

# 🇪🇸 Sección en Español

# Tu Servidor de IA en la Nube 24/7
### Guía Paso a Paso para Principiantes
**Hermes Agent + Render.com + OpenRouter**

* Elimina las suscripciones de 20€/mes para siempre
* Infraestructura y modelos 100% gratuitos (:free)
* Chat web directo en el servidor (`chat.html`) y acceso móvil por Telegram

---

# ¿Por qué este proyecto?

* **El problema:** ChatGPT Plus o Claude Pro cuestan más de 240€ al año.
* **La solución:**
  * **Hermes Agent (Nous Research):** Memoria persistente y ejecución autónoma.
  * **OpenRouter:** Modelos punteros (Llama 3.3 70B, Gemini Flash) a coste 0.00€.
  * **Render.com:** Alojamiento en la nube con 750 horas gratis al mes.
  * **Chat Web en el Servidor (`chat.html`):** Alojado directamente en tu dominio.

---

# Paso 1: Clave de OpenRouter

1. Entra en **[openrouter.ai](https://openrouter.ai)** y pulsa **Sign In**.
2. Ve a **[openrouter.ai/keys](https://openrouter.ai/keys)**.
3. Haz clic en **Create Key**:
   * Nombre: `Hermes Gratis`
   * Límite de crédito: *Déjalo en blanco*
4. Copia tu clave secreta que empieza por `sk-or-v1-...`.

---

# Paso 2: Bot de Telegram (Opcional)

1. En Telegram, busca **`@BotFather`** y envía `/newbot`.
2. Dale un nombre visible y un nombre de usuario que termine en `bot`.
3. Guarda el **HTTP API Token** proporcionado.
4. En Telegram, busca **`@userinfobot`**, pulsa Iniciar y copia tu **Id** numérico para restringir el acceso.

---

# Paso 3: Despliegue en Render.com

1. Regístrate en **[render.com](https://render.com)**.
2. En el panel, pulsa en **+ New** ➔ **Web Service**.
3. Conecta este repositorio de GitHub (Render detecta automáticamente el `Dockerfile` en la raíz) o elige **Existing Image**:
   ```text
   docker.io/nousresearch/hermes-agent:latest
   ```
4. Elige el plan **Free ($0/month)**.

---

# Paso 3 (Cont.): Variables en Render

| Variable | Valor |
| :--- | :--- |
| `OPENROUTER_API_KEY` | *(Tu clave `sk-or-v1-...`)* |
| `MODEL_NAME` | `meta-llama/llama-3.3-70b-instruct:free` |
| `PORT` | `10000` |
| `API_SERVER_KEY` | *(Tu contraseña secreta)* |
| `TELEGRAM_BOT_TOKEN` | *(De @BotFather - opcional)* |
| `TELEGRAM_ALLOWED_USERS` | *(Tu ID numérico de Telegram - opcional)* |

Haz clic en **Create Web Service**. ¡En 2 minutos estará en verde (**Live**)!

---

# Paso 4: Chat Web en el Servidor (`chat.html`)

* Entra desde tu navegador a tu URL de Render:
  ```text
  https://tu-servicio.onrender.com
  ```
* Introduce tu contraseña `API_SERVER_KEY` una sola vez.
* **Ventajas:**
  * Conexión directa al origen (`/v1/chat/completions`).
  * Sin problemas de CORS.
  * Accesible desde cualquier ordenador, móvil o tablet sin instalar nada.

---

# Clientes Web Alternativos

* **Archivo local (`web/chat_web.html`):**
  Doble clic en el archivo HTML en tu ordenador. Introduce tu URL de Render y tu clave.
* **NextChat Web:**
  Entra en [app.nextchat.dev](https://app.nextchat.dev). En Ajustes, selecciona Custom OpenAI y pon `https://tu-servicio.onrender.com/v1`.
* **Telegram Web:**
  Entra en [web.telegram.org](https://web.telegram.org) para chatear con tu bot en cualquier navegador.

---

# Mantenerlo Activo 24/7

1. Copia tu URL de Render (`https://tu-servicio.onrender.com`).
2. Crea una cuenta gratuita en [cron-job.org](https://cron-job.org).
3. Programa un ping HTTP GET cada **10 minutos**.
4. ¡Tu servidor responderá al instante las 24 horas del día sin dormirse!

---

# Resumen de lo Conseguido

✅ **Coste Cero:** 0€ al mes para siempre, sin tarjeta bancaria.
✅ **Potencia Máxima:** Inteligencia de código abierto de 70B parámetros.
✅ **Flexibilidad:** Chat web en servidor, HTML local y bot de Telegram.
✅ **Soberanía:** Tu contenedor privado, tus datos y tus claves.

🎉 **¡Enhorabuena! Has conquistado tu independencia de las suscripciones.**
