// FarmGuard X - Service Worker (Offline Cache Engine)

const CACHE_NAME = 'farmguard-x-offline-v2';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './styles.css',
  './app.js',
  './manifest.json',
  './assets/tomato_late_blight.jpg',
  './assets/healthy_tomato.jpg',
  './assets/tomato_early_blight.jpg',
  './assets/tomato_bacterial_spot.jpg',
  './assets/tomato_yellow_leaf_curl.jpg',
  './assets/potato_early_blight.jpg',
  './assets/potato_late_blight.jpg',
  './assets/potato_healthy.jpg'
];

// Service Worker Installation
self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Installing Offline Engine...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] Pre-caching core application assets...');
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

// Service Worker Activation
self.addEventListener('activate', (event) => {
  console.log('[ServiceWorker] Activating Offline Engine...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log('[ServiceWorker] Clearing old cache:', cache);
            return caches.delete(cache);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Cache-First Strategy with Network Fallback
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then((networkResponse) => {
        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
          return networkResponse;
        }
        const responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache);
        });
        return networkResponse;
      }).catch(() => {
        // Offline Fallback for html pages
        if (event.request.headers.get('accept').includes('text/html')) {
          return caches.match('./index.html');
        }
      });
    })
  );
});
