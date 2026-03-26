const CACHE = 'heillon-lc2s-v1'
const ASSETS = ['/app.html', '/manifest.json']

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)))
  self.skipWaiting()
})

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ))
  self.clients.claim()
})

self.addEventListener('fetch', e => {
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  )
})

// Push notifications
self.addEventListener('push', e => {
  const data = e.data?.json() || {}
  const title = data.title || 'HEILLON LC²S'
  const opts = {
    body: data.body || 'Nova ação avaliada pelo LC²S',
    icon: '/icon-192.png',
    badge: '/icon-192.png',
    data: data,
    vibrate: [100, 50, 100],
    tag: 'lc2s-action',
    renotify: true,
    actions: [
      { action: 'view', title: 'Ver veredito' },
      { action: 'dismiss', title: 'Ignorar' }
    ]
  }
  e.waitUntil(self.registration.showNotification(title, opts))
})

self.addEventListener('notificationclick', e => {
  e.notification.close()
  if (e.action === 'view' || !e.action) {
    e.waitUntil(clients.openWindow('/app.html'))
  }
})
