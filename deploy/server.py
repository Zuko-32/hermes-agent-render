#!/usr/bin/env python3
"""
Hermes Agent On-Server Web Gateway, Dashboard & Reverse Proxy
- Serves chat.html at '/' and '/chat'
- Serves presentation.html at '/presentation'
- Proxies '/dashboard', '/api/*', and SPA routes to the Hermes Web Dashboard (port 9119)
- Tunnels WebSockets ('/api/ws', '/api/pty') for reactive dashboard and embedded TUI terminal
- Proxies '/v1/*' to the Hermes Gateway (port 8642) with OpenRouter fallback
"""

import http.server
import socketserver
import urllib.request
import urllib.error
import socket
import select
import json
import os
import sys

PORT = int(os.environ.get("PORT", 10000))
GATEWAY_PORT = int(os.environ.get("HERMES_GATEWAY_PORT", 8642))
DASHBOARD_PORT = int(os.environ.get("HERMES_DASHBOARD_PORT", 9119))
API_SERVER_KEY = os.environ.get("API_SERVER_KEY", "").strip()
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_HTML_PATH = os.path.join(BASE_DIR, "../web/chat.html")
if not os.path.exists(CHAT_HTML_PATH):
    CHAT_HTML_PATH = "/opt/hermes/web/chat.html"

CHAT_WEB_HTML_PATH = os.path.join(BASE_DIR, "../web/chat_web.html")
if not os.path.exists(CHAT_WEB_HTML_PATH):
    CHAT_WEB_HTML_PATH = "/opt/hermes/web/chat_web.html"

PRESENTATION_HTML_PATH = os.path.join(BASE_DIR, "../web/presentation.html")
if not os.path.exists(PRESENTATION_HTML_PATH):
    PRESENTATION_HTML_PATH = "/opt/hermes/web/presentation.html"

DOCS_HTML_PATH = os.path.join(BASE_DIR, "../docs/index.html")
if not os.path.exists(DOCS_HTML_PATH):
    DOCS_HTML_PATH = "/opt/hermes/docs/index.html"

DASHBOARD_ROUTES = (
    "/dashboard",
    "/config",
    "/env",
    "/api-keys",
    "/sessions",
    "/logs",
    "/analytics",
    "/cron",
    "/profiles",
    "/skills",
    "/mcp",
    "/webhooks",
    "/pairing",
    "/channels",
    "/system",
    "/assets",
    "/vite.svg",
    "/favicon.ico"
)

class HermesProxyHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

    def is_websocket_upgrade(self):
        upgrade = self.headers.get("Upgrade", "").lower()
        connection = self.headers.get("Connection", "").lower()
        return "websocket" in upgrade or "upgrade" in connection

    def tunnel_websocket(self, target_port):
        backend_sock = None
        try:
            backend_sock = socket.create_connection(("127.0.0.1", target_port), timeout=10)
            req_line = f"{self.command} {self.path} {self.request_version}\r\n"
            headers_str = "".join(f"{k}: {v}\r\n" for k, v in self.headers.items())
            backend_sock.sendall((req_line + headers_str + "\r\n").encode("utf-8"))

            client_sock = self.connection
            socks = [client_sock, backend_sock]
            while True:
                readable, _, errored = select.select(socks, [], socks, 60.0)
                if errored or not readable:
                    break
                for s in readable:
                    data = s.recv(65536)
                    if not data:
                        return
                    other = backend_sock if s is client_sock else client_sock
                    other.sendall(data)
        except Exception as e:
            sys.stderr.write(f"[!] WebSocket tunnel error: {e}\n")
        finally:
            if backend_sock:
                try:
                    backend_sock.close()
                except Exception:
                    pass

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):
        if self.is_websocket_upgrade():
            self.tunnel_websocket(DASHBOARD_PORT)
            return

        clean_path = self.path.split("?")[0].rstrip("/")
        if clean_path in ("", "/index.html", "/chat", "/chat.html"):
            self.serve_chat_html()
            return
        elif clean_path in ("/chat_web", "/chat_web.html"):
            self.serve_chat_web_html()
            return
        elif clean_path in ("/presentation", "/presentation.html"):
            self.serve_presentation_html()
            return
        elif clean_path in ("/docs", "/docs/index.html", "/documentation", "/docs.html"):
            self.serve_docs_html()
            return
        elif clean_path in ("/healthz", "/health"):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"OK")
            return
        elif self.path.startswith("/v1/models"):
            self.handle_models()
            return
        elif self.path.startswith("/v1/"):
            self.forward_request("GET", GATEWAY_PORT)
            return
        elif self.path.startswith("/api/"):
            self.forward_dashboard_request("GET")
            return
        elif self.is_dashboard_path():
            self.forward_dashboard_request("GET")
            return
        else:
            self.forward_request("GET", GATEWAY_PORT)

    def do_POST(self):
        if self.is_websocket_upgrade():
            self.tunnel_websocket(DASHBOARD_PORT)
            return

        if self.path.startswith("/v1/"):
            self.forward_request("POST", GATEWAY_PORT)
        elif self.path.startswith("/api/") or self.is_dashboard_path():
            self.forward_dashboard_request("POST")
        else:
            self.forward_request("POST", GATEWAY_PORT)

    def do_PUT(self):
        if self.path.startswith("/api/") or self.is_dashboard_path():
            self.forward_dashboard_request("PUT")
        else:
            self.forward_request("PUT", GATEWAY_PORT)

    def do_DELETE(self):
        if self.path.startswith("/api/") or self.is_dashboard_path():
            self.forward_dashboard_request("DELETE")
        else:
            self.forward_request("DELETE", GATEWAY_PORT)

    def do_PATCH(self):
        if self.path.startswith("/api/") or self.is_dashboard_path():
            self.forward_dashboard_request("PATCH")
        else:
            self.forward_request("PATCH", GATEWAY_PORT)

    def is_dashboard_path(self):
        clean_path = self.path.split("?")[0]
        if clean_path == "/dashboard" or clean_path.startswith("/dashboard/"):
            return True
        for route in DASHBOARD_ROUTES:
            if clean_path == route or clean_path.startswith(route + "/"):
                return True
        return False

    def serve_chat_html(self):
        if os.path.exists(CHAT_HTML_PATH):
            with open(CHAT_HTML_PATH, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"chat.html not found.")

    def serve_chat_web_html(self):
        if os.path.exists(CHAT_WEB_HTML_PATH):
            with open(CHAT_WEB_HTML_PATH, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"chat_web.html not found.")

    def serve_presentation_html(self):
        if os.path.exists(PRESENTATION_HTML_PATH):
            with open(PRESENTATION_HTML_PATH, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"presentation.html not found.")

    def serve_docs_html(self):
        if os.path.exists(DOCS_HTML_PATH):
            with open(DOCS_HTML_PATH, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"docs/index.html not found.")

    def handle_models(self):
        target_url = f"http://127.0.0.1:{GATEWAY_PORT}/v1/models"
        try:
            req = urllib.request.Request(target_url, headers=self.build_forward_headers(), method="GET")
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = resp.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)
                return
        except Exception:
            pass

        fallback_models = {
            "object": "list",
            "data": [
                {"id": "openrouter/free", "object": "model", "owned_by": "hermes-agent"},
                {"id": "meta-llama/llama-3.3-70b-instruct:free", "object": "model", "owned_by": "meta"},
                {"id": "google/gemini-2.0-flash-exp:free", "object": "model", "owned_by": "google"},
                {"id": "deepseek/deepseek-r1:free", "object": "model", "owned_by": "deepseek"},
                {"id": "qwen/qwen-2.5-coder-32b-instruct:free", "object": "model", "owned_by": "qwen"}
            ]
        }
        encoded = json.dumps(fallback_models).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(encoded)

    def build_forward_headers(self):
        headers = {}
        has_auth = False
        for k, v in self.headers.items():
            if k.lower() == "host":
                continue
            if k.lower() == "authorization":
                has_auth = True
                headers[k] = v
            else:
                headers[k] = v

        if (not has_auth or headers.get("Authorization") in ("Bearer", "Bearer null", "Bearer undefined")) and API_SERVER_KEY:
            headers["Authorization"] = f"Bearer {API_SERVER_KEY}"

        return headers

    def forward_dashboard_request(self, method):
        # Handle /dashboard or /dashboard/* rewritten path
        target_path = self.path
        if target_path == "/dashboard" or target_path == "/dashboard/":
            target_path = "/"
        elif target_path.startswith("/dashboard/"):
            target_path = target_path[len("/dashboard"):]

        target_url = f"http://127.0.0.1:{DASHBOARD_PORT}{target_path}"
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else None

        req_headers = self.build_forward_headers()
        req = urllib.request.Request(target_url, data=post_data, headers=req_headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                self.send_response(response.status)
                for header, value in response.headers.items():
                    if header.lower() not in ("transfer-encoding", "content-length", "access-control-allow-origin"):
                        self.send_header(header, value)
                resp_body = response.read()
                self.send_header("Content-Length", str(len(resp_body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("X-Hermes-Backend", "Web-Dashboard")
                self.end_headers()
                self.wfile.write(resp_body)
                return

        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for header, value in e.headers.items():
                if header.lower() not in ("transfer-encoding", "content-length", "access-control-allow-origin"):
                    self.send_header(header, value)
            err_body = e.read()
            self.send_header("Content-Length", str(len(err_body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(err_body)
            return

        except Exception as ex:
            print(f"[!] Dashboard 127.0.0.1:{DASHBOARD_PORT} unreachable: {ex}")
            log_snippet = ""
            if os.path.exists("/tmp/hermes-dashboard.log"):
                try:
                    with open("/tmp/hermes-dashboard.log", "r", errors="ignore") as f:
                        log_snippet = "".join(f.readlines()[-30:])
                except Exception:
                    pass

            is_browser_request = "text/html" in self.headers.get("Accept", "")
            if is_browser_request:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="3">
  <title>HERMES DASHBOARD // INITIALIZING</title>
  <style>
    body {{
      background: #07090e;
      color: #f4f4f6;
      font-family: 'JetBrains Mono', monospace;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
      padding: 20px;
      box-sizing: border-box;
      text-align: center;
    }}
    .box {{
      max-width: 680px;
      border: 1px solid rgba(0, 240, 255, 0.4);
      background: rgba(14, 19, 30, 0.95);
      padding: 30px;
      border-radius: 4px;
      box-shadow: 0 0 30px rgba(0, 240, 255, 0.15);
    }}
    h1 {{ font-size: 1.2rem; color: #00f0ff; margin-bottom: 12px; }}
    p {{ font-size: 0.85rem; color: #8e95a5; line-height: 1.6; margin-bottom: 20px; }}
    pre {{
      background: #04060a;
      border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 12px;
      text-align: left;
      font-size: 0.75rem;
      color: #c6f135;
      overflow-x: auto;
      max-height: 200px;
    }}
    .btn {{
      display: inline-block;
      margin-top: 15px;
      padding: 8px 16px;
      background: #00f0ff;
      color: #000;
      text-decoration: none;
      font-weight: bold;
      border-radius: 2px;
    }}
  </style>
</head>
<body>
  <div class="box">
    <h1>[ 🎛 HERMES WEB DASHBOARD // STARTING UP ]</h1>
    <p>The internal Hermes Web Dashboard process (port {DASHBOARD_PORT}) is currently initializing.<br>
    This page will automatically refresh every 3 seconds until ready.</p>
    <pre>{log_snippet or "Starting hermes dashboard on 127.0.0.1:9119..."}</pre>
    <a href="/" class="btn">➔ RETURN TO CHAT CONSOLE</a>
  </div>
</body>
</html>"""
                self.wfile.write(html.encode("utf-8"))
                return

            self.send_response(503)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            payload = {
                "error": f"Hermes Web Dashboard initializing on port {DASHBOARD_PORT}",
                "message": "The dashboard process is starting up. Please retry in a few seconds.",
                "dashboard_log": log_snippet or "No dashboard logs yet."
            }
            self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))

    def forward_request(self, method, target_port):
        target_url = f"http://127.0.0.1:{target_port}{self.path}"
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else None

        req_headers = self.build_forward_headers()
        req = urllib.request.Request(target_url, data=post_data, headers=req_headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                self.send_response(response.status)
                for header, value in response.headers.items():
                    if header.lower() not in ("transfer-encoding", "content-length", "access-control-allow-origin"):
                        self.send_header(header, value)
                resp_body = response.read()
                self.send_header("Content-Length", str(len(resp_body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("X-Hermes-Backend", "Local-Gateway")
                self.end_headers()
                self.wfile.write(resp_body)
                return

        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for header, value in e.headers.items():
                if header.lower() not in ("transfer-encoding", "content-length", "access-control-allow-origin"):
                    self.send_header(header, value)
            err_body = e.read()
            self.send_header("Content-Length", str(len(err_body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(err_body)
            return

        except Exception as ex:
            print(f"[!] Target 127.0.0.1:{target_port} unreachable: {ex}")

            # Direct OpenRouter Fallback for chat completions if OPENROUTER_API_KEY exists
            if self.path.startswith("/v1/chat/completions") and OPENROUTER_API_KEY and post_data:
                try:
                    print("[*] Attempting direct OpenRouter upstream fallback...")
                    or_url = "https://openrouter.ai/api/v1/chat/completions"
                    or_headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "HTTP-Referer": "https://render.com",
                        "X-Title": "Hermes Agent Render"
                    }
                    or_req = urllib.request.Request(or_url, data=post_data, headers=or_headers, method="POST")
                    with urllib.request.urlopen(or_req, timeout=60) as or_res:
                        self.send_response(or_res.status)
                        for h, v in or_res.headers.items():
                            if h.lower() not in ("transfer-encoding", "content-length", "access-control-allow-origin"):
                                self.send_header(h, v)
                        or_body = or_res.read()
                        self.send_header("Content-Length", str(len(or_body)))
                        self.send_header("Access-Control-Allow-Origin", "*")
                        self.send_header("X-Hermes-Backend", "OpenRouter-Fallback")
                        self.end_headers()
                        self.wfile.write(or_body)
                        return
                except Exception as or_err:
                    print(f"[!] OpenRouter fallback failed: {or_err}")

            log_snippet = ""
            for log_file in ("/tmp/hermes-gateway.log", "/opt/data/gateway.log"):
                if os.path.exists(log_file):
                    try:
                        with open(log_file, "r", errors="ignore") as f:
                            lines = f.readlines()
                            log_snippet = "".join(lines[-40:])
                        break
                    except Exception:
                        pass

            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            payload = {
                "error": f"Hermes Gateway unavailable: {str(ex)}",
                "hint": "The internal gateway process is initializing. If the Render instance recently awoke from cold sleep, please wait 20-30 seconds and retry.",
                "gateway_log": log_snippet or "No gateway logs recorded."
            }
            self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), HermesProxyHandler) as httpd:
        print(f"[*] Hermes Unified Proxy running on http://0.0.0.0:{PORT}")
        print(f"[*] - Chat Console: '/' and '/chat'")
        print(f"[*] - Interactive Presentation: '/presentation'")
        print(f"[*] - Web Dashboard & REST API: '/dashboard', '/api/*', and SPA routes (Port {DASHBOARD_PORT})")
        print(f"[*] - Inference Gateway: '/v1/*' (Port {GATEWAY_PORT})")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
