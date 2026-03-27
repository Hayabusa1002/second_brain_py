const CACHE_NAME = "second-brain-v1"

// Static assets that do not require auth
const STATIC_ASSETS = [
    "/login",
    "/register",
    "https://cdn.jsdelivr.net/npm/@tabler/core@1.4.0/dist/css/tabler.min.css",
    "https://cdn.jsdelivr.net/npm/@tabler/core@1.4.0/dist/js/tabler.min.js",
]

// API routes to cache once the user is authenticated
const API_CACHE_ROUTES = [
    "/api/transactions",
    "/api/accounts",
    "/api/categories",
    "/api/auth/me",
]

// Pages that require auth — never cache their response to avoid storing redirects
const AUTH_REQUIRED_PAGES = ["/", "/accounts", "/users", "/change-password", "/access-requests"]


// ── Install ───────────────────────────────────────────────────────────────────
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
    )
    self.skipWaiting()
})


// ── Activate ──────────────────────────────────────────────────────────────────
self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(
                keys
                    .filter((key) => key !== CACHE_NAME)
                    .map((key) => caches.delete(key))
            )
        )
    )
    self.clients.claim()
})


// ── Fetch ─────────────────────────────────────────────────────────────────────
self.addEventListener("fetch", (event) => {
    const { request } = event
    const url = new URL(request.url)

    // Only intercept GET requests from the same origin or jsDelivr CDN
    if (request.method !== "GET") return
    if (url.origin !== self.location.origin && !request.url.includes("cdn.jsdelivr.net")) return

    // Auth-required pages → always fetch from network, never cache
    const isAuthPage = AUTH_REQUIRED_PAGES.some((p) => url.pathname === p)
    if (isAuthPage) {
        event.respondWith(fetch(request))
        return
    }

    // API routes → network first, fallback to cache
    const isApiRoute = API_CACHE_ROUTES.some((route) => url.pathname.startsWith(route))
    if (isApiRoute) {
        event.respondWith(networkFirstWithCache(request))
        return
    }

    // Static assets and public pages → cache first, fallback to network
    event.respondWith(cacheFirstWithNetwork(request))
})


async function networkFirstWithCache(request) {
    const cache = await caches.open(CACHE_NAME)
    try {
        const networkResponse = await fetch(request)
        // Do not cache redirects
        if (networkResponse.ok && networkResponse.type !== "opaqueredirect") {
            cache.put(request, networkResponse.clone())
        }
        return networkResponse
    } catch {
        // No connection — return cached response if available
        const cached = await cache.match(request)
        return cached || new Response(
            JSON.stringify({ detail: "Offline. Showing cached data." }),
            { status: 503, headers: { "Content-Type": "application/json" } }
        )
    }
}


async function cacheFirstWithNetwork(request) {
    const cached = await caches.match(request)
    if (cached) return cached

    try {
        const networkResponse = await fetch(request)
        // Do not cache redirects
        if (networkResponse.ok && networkResponse.type !== "opaqueredirect") {
            const cache = await caches.open(CACHE_NAME)
            cache.put(request, networkResponse.clone())
        }
        return networkResponse
    } catch {
        // Fallback to login page or plain error
        return caches.match("/login") || new Response(
            "<h1>Offline</h1><p>Check your connection and try again.</p>",
            { status: 503, headers: { "Content-Type": "text/html" } }
        )
    }
}