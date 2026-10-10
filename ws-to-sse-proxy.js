// ws-to-sse-proxy.js
const express = require('express');
const WebSocket = require('ws');

const REMOTE_WS = process.env.REMOTE_MCP_WS || 'ws://89.6.129.67:3000';
const PORT = parseInt(process.env.PORT || '10000', 10);
const API_KEY = process.env.MCP_API_KEY || null;

const app = express();

app.get('/mcp', (req, res) => {
  res.set({
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    Connection: 'keep-alive'
  });
  res.flushHeaders();

  // Autenticación opcional
  const token = req.query.api_key || req.headers['x-api-key'];
  if (API_KEY && token !== API_KEY) {
    res.statusCode = 401;
    res.end('Unauthorized\n');
    return;
  }

  const ws = new WebSocket(REMOTE_WS);

  const send = (data) => {
    try {
      const payload = typeof data === 'string' ? data : JSON.stringify(data);
      res.write(`data: ${payload}\n\n`);
    } catch (e) {}
  };

  ws.on('open', () => send({ type: 'proxy', status: 'connected' }));
  ws.on('message', (msg) => send(msg));
  ws.on('error', (err) => {
    try { res.write(`event: error\ndata: ${JSON.stringify({ error: String(err) })}\n\n`); } catch (e) {}
    try { res.end(); } catch (e) {}
  });
  ws.on('close', () => { try { res.end(); } catch (e) {} });

  req.on('close', () => {
    try { ws.close(); } catch (e) {}
  });
});

app.get('/healthz', (req, res) => res.json({ ok: true }));

app.listen(PORT, '0.0.0.0', () => {
  console.log(`SSE proxy listening on 0.0.0.0:${PORT}, proxying ${REMOTE_WS}`);
});
