const CACHE_NAME = "c2c-pwa-v1";

const FILES_TO_CACHE = [
    "./",
    "./index.html",
    "./manifest.webmanifest"
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(FILES_TO_CACHE);
        })
    );

    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", (event) => {
    if (event.request.method === "GET") {
        event.respondWith(
            fetch(event.request).catch(() => caches.match(event.request))
        );
    }
});
