#!/usr/bin/env node
const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 10000;

// Serve static files from ./web
app.use(express.static(path.join(__dirname, 'web')));

// Root serves the main HTML (adjust filename if needed)
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'web', 'chat_web.html'));
});

// Mount the SSE proxy module (ws-to-sse-proxy.js must export a function)
try {
  const mountProxy = require('./ws-to-sse-proxy');
  if (typeof mountProxy === 'function') {
    mountProxy(app);
  } else {
    console.warn('ws-to-sse-proxy.js does not export a function. Check the module.');
  }
} catch (err) {
  console.error('Failed to mount ws-to-sse-proxy:', err);
}

// Healthcheck
app.get('/healthz', (req, res) => res.json({ ok: true }));

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`HTTP + SSE server listening on ${PORT}`);
});
