const CACHE = 'heillon-companion-v2';
const ASSETS = ['/', '/app.html', '/manifest.json', '/icon-192.png', '/icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).catch(()=>{}));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ));
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  if (e.request.url.includes('railway.app')) return;
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request).catch(() => cached))
  );
});

// ── PUSH NOTIFICATIONS ───────────────────────────────────────────────────────
self.addEventListener('push', e => {
  let data = { title: 'HEILLON', body: 'Nova decisão soberana', hdr_id: null, verdict: 'ALLOW' };
  try { data = { ...data, ...e.data.json() }; } catch (_) {}

  const isBlocked = data.verdict === 'BLOCKED' || data.verdict === 'denied';
  const icon = '/icon-192.png';
  const badge = '/icon-192.png';

  e.waitUntil(
    self.registration.showNotification(data.title || 'HEILLON', {
      body: data.body || (isBlocked ? '✗ Ação bloqueada' : '✓ Decisão autorizada'),
      icon,
      badge,
      tag: 'heillon-hdr',          // substitui a anterior — só 1 notif por vez
      renotify: true,
      data: { hdr_id: data.hdr_id, url: '/app.html' },
      actions: [
        { action: 'view', title: 'Ver HDR' },
        { action: 'dismiss', title: 'Dispensar' },
      ],
      vibrate: isBlocked ? [100, 50, 200, 50, 100] : [50, 30, 80],
    })
  );
});

self.addEventListener('notificationclick', e => {
  e.notification.close();
  if (e.action === 'dismiss') return;
  e.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(wins => {
      const existing = wins.find(w => w.url.includes('/app.html'));
      if (existing) { existing.focus(); return; }
      return clients.openWindow('/app.html');
    })
  );
});
