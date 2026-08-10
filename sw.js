const CACHE_NAME = 'nikki-ai-v1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './web_gui/style.css',
  './web_gui/app.js',
  './assets/nikki_avatar.jpg',
  './manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
