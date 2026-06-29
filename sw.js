const CACHE = 'learning-games-v1';
const FILES = [
    './index.html',
    './game2.html',
    './game3.html',
    './manifest.json',
    './icons/icon-180.png',
    './icons/icon-192.png',
    './icons/icon-512.png',
];

self.addEventListener('install', e => {
    e.waitUntil(
        caches.open(CACHE).then(c => c.addAll(FILES))
    );
    self.skipWaiting();
});

self.addEventListener('activate', e => {
    e.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
        )
    );
    self.clients.claim();
});

self.addEventListener('fetch', e => {
    e.respondWith(
        caches.match(e.request).then(cached => cached || fetch(e.request).catch(() => caches.match('./index.html')))
    );
});
