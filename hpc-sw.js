// HEILLON HPC — Service Worker
// Intercepta requests de rede dentro do domínio hpc.heillon.com
// e detecta automaticamente domínios de IAs conhecidas

const AI_DOMAINS = {
  'api.openai.com': 'chatgpt',
  'chatgpt.com': 'chatgpt',
  'chat.openai.com': 'chatgpt',
  'claude.ai': 'claude',
  'api.anthropic.com': 'claude',
  'gemini.google.com': 'gemini',
  'generativelanguage.googleapis.com': 'gemini',
  'copilot.microsoft.com': 'copilot',
  'bing.com': 'copilot',
  'x.ai': 'grok',
  'grok.com': 'grok',
  'perplexity.ai': 'perplexity',
  'api.mistral.ai': 'mistral',
};

const CACHE = 'heillon-hpc-v1';

self.addEventListener('install', e => {
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(clients.claim());
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  const hostname = url.hostname.replace('www.', '');

  // Detectar domínio de IA
  for (const [domain, aiKey] of Object.entries(AI_DOMAINS)) {
    if (hostname.includes(domain)) {
      // Notificar todas as tabs abertas do HPC
      self.clients.matchAll({ type: 'window' }).then(clients => {
        clients.forEach(client => {
          client.postMessage({ type: 'AI_DETECTED', ai: aiKey, domain: hostname });
        });
      });
      break;
    }
  }

  // Pass-through — não bloquear nada
  e.respondWith(fetch(e.request));
});
