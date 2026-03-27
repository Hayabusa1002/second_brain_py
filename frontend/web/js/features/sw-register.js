if ("serviceWorker" in navigator) {
    window.addEventListener("load", async () => {
        try {
            const reg = await navigator.serviceWorker.register("/static/sw.js", {
                scope: "/",
            })
            console.log("[SW] Registered:", reg.scope)
        } catch (err) {
            console.warn("[SW] Register error:", err)
        }
    })
}