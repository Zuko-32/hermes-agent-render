// ws-to-sse-proxy.js
const WebSocket = require('ws');

module.exports = function mountWsToSse(app, options = {}) {
  const REMOTE_WS = options.remote || process.env.REMOTE_MCP_WS || 'ws://89.6.129.67:3000';
  const API_KEY = process.env.MCP_API_KEY || null;

  app.get('/mcp', (req, res) => {
    res.set({
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive'
    });
    res.flushHeaders();

    const token = req.query.api_key || req.headers['x-api-key'];
    if (API_KEY && token !== API_KEY) {
      res.status(401).end('Unauthorized\n');
      return;
    }

    const ws = new WebSocket(REMOTE_WS);

    const send = (data) => {
      try {
        const payload = Buffer.isBuffer(data) ? data.toString('utf8') : data;
        // si payload es JSON string, lo enviamos tal cual; si es objeto, lo stringify
        const out = typeof payload === 'string' ? payload : JSON.stringify(payload);
        res.write(`data: ${out}\n\n`);
      } catch (e) {
        console.error('SSE send error', e);
      }
    };

    ws.on('open', () => send(JSON.stringify({ type: 'proxy', status: 'connected' })));
    ws.on('message', (msg) => send(msg));
    ws.on('error', (err) => {
      console.error('WS error', err);
      try { res.write(`event: error\ndata: ${JSON.stringify({ error: String(err) })}\n\n`); } catch (e) {}
      try { res.end(); } catch (e) {}
    });
    ws.on('close', () => { try { res.end(); } catch (e) {} });

    req.on('close', () => {
      try { if (ws && ws.readyState === WebSocket.OPEN) ws.close(); } catch (e) {}
    });
  });
};

