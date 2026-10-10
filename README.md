# ⚡ Free 24/7 Autonomous AI Agent on Render & OpenRouter

[![Render](https://img.shields.io/badge/Render-Live%20Service-46E3B7?logo=render&logoColor=white)](https://hermes-agent-render-a9ab.onrender.com)
[![Web Chat](https://img.shields.io/badge/Web%20Chat-Live%20Console-00f0ff?logo=safari&logoColor=black)](https://hermes-agent-render-a9ab.onrender.com/)
[![Master Docs](https://img.shields.io/badge/Master%20Docs-Live%20HTML-c6f135?logo=readme&logoColor=black)](https://hermes-agent-render-a9ab.onrender.com/docs)
[![Interactive Slides](https://img.shields.io/badge/Interactive%20Slides-Live%20Presentation-ff3366?logo=google-slides&logoColor=white)](https://hermes-agent-render-a9ab.onrender.com/presentation)
[![Hermes Dashboard](https://img.shields.io/badge/Hermes-Web%20Dashboard-38BDF8?logo=speedtest&logoColor=white)](https://hermes-agent-render-a9ab.onrender.com/dashboard)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Free%20Models-6366F1?logo=openai&logoColor=white)](https://openrouter.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Deploy your personal, persistent, autonomous AI assistant in the cloud for $0/month, powered by Nous Research's Hermes Agent and OpenRouter's free-tier models (`:free`).**

---

## 🌐 Language Navigation / Navegación por Idioma
- [English Documentation](#-english-documentation)
- [Documentación en Español](#-documentación-en-español)

---

# 🇬🇧 English Documentation

## Overview

This repository contains everything needed to deploy and run **Hermes Agent** (by Nous Research) on **Render.com** (Free Plan) utilizing **OpenRouter**'s free-tier models (`:free`).

Say goodbye to recurring $20+/month subscriptions like ChatGPT Plus or Claude Pro. You can now operate your own private AI assistant 24/7 accessible from:
1. **Any Web Browser** (via the on-server console `chat.html` at [hermes-agent-render-a9ab.onrender.com](https://hermes-agent-render-a9ab.onrender.com) or standalone client `chat_web.html`).
2. **Hermes Web Dashboard** (full visual control over config, skills, MCP, cron, logs, and terminal at [/dashboard](https://hermes-agent-render-a9ab.onrender.com/dashboard)).
3. **Telegram** (as a personal private bot on your smartphone or desktop).

---

## Key Features

- **Cost: $0.00 / Month Forever**: Runs on Render's 750 free monthly instance hours with OpenRouter `:free` models. No credit card required.
- **Persistent Memory & Tools**: Hermes Agent remembers conversations, builds skills, and executes multi-step workflows.
- **Swiss Modernist Interface**: Inspired by [seunghyuk.com](https://seunghyuk.com/?ref=siteinspire) with 32px structural grid, high-contrast dark palette, corner crosshairs (`+`), and `Space Grotesk` + `JetBrains Mono` + `Syne` precision typography.
- **On-Server Web Chat (`chat.html`)**: Built-in console hosted directly on your Render domain ([hermes-agent-render-a9ab.onrender.com](https://hermes-agent-render-a9ab.onrender.com)). Features multi-session chat history, real-time persistence (zero data loss on page refresh), dynamic free models from OpenRouter, and zero CORS configuration.
- **Hermes Web Dashboard (`/dashboard`)**: Full visual control center. Edit `config.yaml`, manage skills and tools, configure MCP servers, stream live logs, launch interactive browser terminal (PTY), schedule cron jobs, and monitor token analytics.
- **Master HTML Documentation (`/docs`)**: Full-featured bilingual interactive technical documentation website ([hermes-agent-render-a9ab.onrender.com/docs](https://hermes-agent-render-a9ab.onrender.com/docs)) matching the Swiss modernist design with real-time `[EN / ES]` language switching and copyable blueprints.
- **Interactive Presentation (`/presentation`)**: 13-slide modernist visual manual ([hermes-agent-render-a9ab.onrender.com/presentation](https://hermes-agent-render-a9ab.onrender.com/presentation)) with touch swipe gestures and direct configuration downloads.
- **Standalone Web Client (`chat_web.html`)**: Lightweight single-file client to connect to your agent remotely from any browser, complete with persistent conversation history, session management, and configuration storage.
- **Telegram Bot Support**: Send voice notes, files, and text messages directly to your agent from your phone.
- **High-Performance Free Models**: Access Meta Llama 3.3 70B, Google Gemini 2.0 Flash Lite, DeepSeek R1, and Qwen 2.5 Coder at zero cost.

---

## 📁 Repository Structure

```
hermes-agent-render/
├── README.md                      # Project documentation (English & Spanish)
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
├── Dockerfile                     # Custom container (Hermes + Dashboard + Docs + Web Chat) — auto-detected by Render
├── render.yaml                    # Render Blueprint (Infrastructure as Code)
├── docs/
│   ├── index.html                # Master HTML documentation (Bilingual EN/ES Swiss Modernist)
│   ├── MANUAL_HERMES_RENDER.md   # Step-by-step markdown installation manual (EN/ES)
│   └── PRESENTATION_SLIDES.md    # Markdown slide deck for Marp / Slidev
├── web/
│   ├── chat.html                 # Hosted directly on Render (relative endpoints)
│   ├── chat_web.html             # Standalone client for any local browser
│   └── presentation.html         # Interactive slide presentation (Bilingual EN/ES)
├── deploy/
│   ├── Dockerfile                # Deployment container backup
│   ├── server.py                 # Reverse proxy, WebSocket raw TCP tunnel & static server
│   ├── start.sh                  # Process supervisor (Gateway + Web Dashboard + Proxy)
│   ├── docker-compose.yml        # Local or alternative container deployment
│   └── render.yaml               # Render Blueprint backup
└── config/
    └── .env.example              # Environment variables template
```

---

## 📖 Installation & Setup Manual

The full, foolproof setup guide covers everything from obtaining free API keys to deploying on Render with persistent memory and Telegram integration.

👉 **[🚀 Open Master HTML Documentation (Live on Server)](https://hermes-agent-render-a9ab.onrender.com/docs)**
👉 **[Read the Step-by-Step Markdown Manual](docs/MANUAL_HERMES_RENDER.md#-english-manual)**
👉 **[📽 Launch Live Interactive Presentation in Browser](https://hermes-agent-render-a9ab.onrender.com/presentation)**

### What is covered in the manual:
1. **Architecture & Prerequisites**: How Hermes Agent, Render, and OpenRouter work together.
2. **Step 1: Free OpenRouter API Key**: How to generate a `$0.00` key without credit card.
3. **Step 2: Private Telegram Bot**: Create your secure bot via `@BotFather` and lock access to your user ID.
4. **Step 3: Render Deployment**:
   - **Option A (Recommended)**: Connect this GitHub repo (Render auto-detects the root `Dockerfile` and includes `chat.html`, `/dashboard`, and `/docs`).
   - **Option B**: Deploy via Render Blueprint (`render.yaml`).
   - **Option C**: Prebuilt image deployment.
   - Comprehensive environment variables table.
5. **Step 4: Using the On-Server Web Chat (`chat.html`)**: Instant zero-CORS browser chat at `https://hermes-agent-render-a9ab.onrender.com`.
6. **Step 5: Standalone Web Clients (`chat_web.html` & NextChat)**.
7. **Step 6: Hermes Web Dashboard (`/dashboard`)**: Full visual administration, MCP servers, skills, cron jobs, live logs, terminal PTY, and Hermes Desktop connection.
8. **Free Models Catalog (`:free`)**: Llama 3.3 70B, Gemini 2.0 Flash Lite, DeepSeek R1, Qwen 2.5 Coder.
9. **24/7 Keep-Alive**: How to keep Render free tier awake permanently with free pings.
10. **Troubleshooting & FAQ**: Common deployment questions and fixes.

---

## ⚡ 24/7 Keep-Alive Tip
Render's free tier spins down instances after 15 minutes of inactivity. To keep your agent responsive 24/7:
1. Copy your public Render URL: `https://hermes-agent-render-a9ab.onrender.com`.
2. Create a free account on [cron-job.org](https://cron-job.org) or [uptimerobot.com](https://uptimerobot.com).
3. Schedule an automated HTTP GET request to `https://hermes-agent-render-a9ab.onrender.com/healthz` every **10 minutes**.
4. Your server will stay permanently awake with near-zero latency.

---

# 🇪🇸 Documentación en Español

## Visión General

Este repositorio contiene todo lo necesario para desplegar y ejecutar **Hermes Agent** (de Nous Research) en **Render.com** (Plan Gratuito) utilizando los modelos gratuitos de **OpenRouter** (`:free`).

Despídete de pagar 20€/mes por suscripciones como ChatGPT Plus o Claude Pro. Ahora dispones de tu propio asistente de inteligencia artificial funcionando las 24 horas del día, accesible desde:
1. **Cualquier Navegador Web** (mediante la consola `chat.html` en [hermes-agent-render-a9ab.onrender.com](https://hermes-agent-render-a9ab.onrender.com) o el cliente autónomo `chat_web.html`).
2. **Panel de Control Web de Hermes** (control visual integral de config, skills, MCP, cron, logs y terminal en [/dashboard](https://hermes-agent-render-a9ab.onrender.com/dashboard)).
3. **Telegram** (como bot privado en tu smartphone, tablet o PC).

---

## Características Principales

- **Coste: 0,00 € al mes de por vida**: Aprovecha las 750 horas mensuales gratuitas de Render con modelos `:free` de OpenRouter. Sin tarjeta de crédito.
- **Memoria Persistente y Habilidades**: Hermes Agent recuerda conversaciones pasadas, evoluciona sus destrezas y ejecuta flujos de tareas complejas.
- **Diseño Modernista Suizo**: Inspirado en [seunghyuk.com](https://seunghyuk.com/?ref=siteinspire) con retícula estructural de 32px, paleta oscura de alto contraste, cruces de calibración (`+`) y tipografía técnica `Space Grotesk` + `JetBrains Mono` + `Syne`.
- **Chat Web en el Servidor (`chat.html`)**: Interfaz web integrada servida directamente en tu dominio de Render ([hermes-agent-render-a9ab.onrender.com](https://hermes-agent-render-a9ab.onrender.com)). Con historial multi-sesión de chats, persistencia total en tiempo real (cero pérdidas al recargar), catálogo dinámico de modelos de OpenRouter y sin problemas de CORS.
- **Panel de Control Hermes (`/dashboard`)**: Panel de control visual completo para usuarios avanzados. Edita `config.yaml`, gestiona habilidades y herramientas, configura servidores MCP, observa registros en tiempo real, ejecuta la terminal web interactiva PTY, programa tareas cron y analiza el consumo de tokens.
- **Documentación Maestra en HTML (`/docs`)**: Manual técnico visual interactivo bilingüe ([hermes-agent-render-a9ab.onrender.com/docs](https://hermes-agent-render-a9ab.onrender.com/docs)) con conmutador instantáneo de idioma `[EN / ES]`, bloques de código copiables y descargas de plantillas.
- **Presentación Interactiva (`/presentation`)**: Manual visual interactivo de 13 diapositivas ([hermes-agent-render-a9ab.onrender.com/presentation](https://hermes-agent-render-a9ab.onrender.com/presentation)) con gestos táctiles y enlaces directos.
- **Cliente Web Autónomo (`chat_web.html`)**: Archivo HTML único para conectarte remotamente a tu servidor desde cualquier máquina, con historial persistente de conversaciones, gestión de sesiones y almacenamiento de credenciales.
- **Integración con Telegram**: Envía notas de voz, documentos y texto desde tu teléfono a tu agente.
- **Modelos de Primer Nivel Gratuitos**: Llama 3.3 70B, Gemini 2.0 Flash Lite, DeepSeek R1 y Qwen 2.5 Coder sin coste por token.

---

## 📁 Estructura del Repositorio

```
hermes-agent-render/
├── README.md                      # Documentación del proyecto (Inglés y Español)
├── LICENSE                        # Licencia MIT
├── .gitignore                     # Reglas de exclusión de Git
├── Dockerfile                     # Contenedor (Hermes + Dashboard + Docs + Chat Web) — detectado automáticamente por Render
├── render.yaml                    # Render Blueprint (Infraestructura como Código)
├── docs/
│   ├── index.html                # Documentación maestra en HTML (Bilingüe EN/ES estilo Modernista)
│   ├── MANUAL_HERMES_RENDER.md   # Manual maestro paso a paso en Markdown (Inglés y Español)
│   └── PRESENTATION_SLIDES.md    # Diapositivas en Markdown para Marp / Slidev
├── web/
│   ├── chat.html                 # Alojado directamente en Render (rutas relativas)
│   ├── chat_web.html             # Cliente autónomo para cualquier navegador local
│   └── presentation.html         # Presentación de diapositivas interactiva (Bilingüe EN/ES)
├── deploy/
│   ├── Dockerfile                # Copia de seguridad del contenedor
│   ├── server.py                 # Reverse proxy, túnel TCP WebSocket y servidor de archivos estáticos
│   ├── start.sh                  # Supervisor de procesos (Gateway + Web Dashboard + Proxy)
│   ├── docker-compose.yml        # Despliegue en contenedor local o alternativo
│   └── render.yaml               # Copia de seguridad del Blueprint
└── config/
    └── .env.example              # Plantilla de variables de entorno
```

---

## 📖 Manual de Instalación y Despliegue

La guía completa y detallada paso a paso para cualquier usuario (entienda o no de informática) explica todo el proceso desde cero hasta tener el agente funcionando sin coste:

👉 **[🚀 Abrir Documentación Maestra en HTML (En vivo en el servidor)](https://hermes-agent-render-a9ab.onrender.com/docs)**
👉 **[Leer el Manual en Formato Markdown](docs/MANUAL_HERMES_RENDER.md#-manual-en-español)**
👉 **[📽 Abrir Presentación Interactiva en Vivo en el Navegador](https://hermes-agent-render-a9ab.onrender.com/presentation)**

### Qué encontrarás en el manual:
1. **Visión General y Requisitos**: Cómo interactúan Hermes Agent, Render y OpenRouter sin coste.
2. **Paso 1: Clave Gratuita de OpenRouter**: Obtención de credenciales con saldo $0 y sin tarjeta bancaria.
3. **Paso 2: Bot Privado de Telegram**: Configuración en 1 minuto con `@BotFather` y bloqueo seguro por tu ID.
4. **Paso 3: Despliegue en Render.com**:
   - **Opción A (Recomendada)**: Conectar este repositorio de GitHub (Render detecta automáticamente el `Dockerfile` de la raíz e incluye `chat.html`, `/dashboard` y `/docs`).
   - **Opción B**: Despliegue mediante Blueprint (`render.yaml`).
   - **Opción C**: Imagen precompilada directa.
   - Tabla completa de variables de entorno explicadas una a una.
5. **Paso 4: Chat Web en el Servidor (`chat.html`)**: Acceso directo desde cualquier navegador en `https://hermes-agent-render-a9ab.onrender.com`.
6. **Paso 5: Clientes Alternativos (`chat_web.html` y NextChat)**.
7. **Paso 6: Panel de Control Web de Hermes (`/dashboard`)**: Gestión visual completa, servidores MCP, habilidades, tareas cron, registros en vivo, emulador de terminal PTY y conexión con Hermes Desktop.
8. **Catálogo de Modelos Gratuitos (`:free`)**: Llama 3.3 70B, Gemini 2.0 Flash Lite, DeepSeek R1, Qwen 2.5 Coder.
9. **Mantener el Servidor Activo 24/7**: Truco con cron-job gratuito para evitar que Render suspenda la instancia.
10. **Resolución de Dudas y Preguntas Frecuentes**.

---

## ⚡ Estrategia Keep-Alive 24/7
El plan gratuito de Render suspende los contenedores tras 15 minutos sin peticiones entrantes. Para mantener a tu asistente activo y receptivo 24/7 sin latencia de arranque:
1. Copia la URL pública de tu servicio en Render: `https://hermes-agent-render-a9ab.onrender.com`.
2. Crea una cuenta gratuita en [cron-job.org](https://cron-job.org) o [uptimerobot.com](https://uptimerobot.com).
3. Configura un ping HTTP GET recurrente a `https://hermes-agent-render-a9ab.onrender.com/healthz` cada **10 minutos**.
4. Tu agente permanecerá permanentemente despierto sin coste adicional.

---

## 📄 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE). Eres libre de modificarlo, adaptarlo y compartirlo.
