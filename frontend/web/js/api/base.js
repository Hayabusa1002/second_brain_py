export async function fetchWithAuth(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        credentials: "include",  // sends httpOnly cookie automatically
        headers: { ...options.headers }
    })

    if (response.status === 401) {
        window.location.href = "/login"
        return null
    }

    return response
}

const logoutBtn = document.getElementById("btn-logout")
if (logoutBtn) {
    logoutBtn.addEventListener("click", async () => {
        await fetch("/api/auth/logout", {
            method: "POST",
            credentials: "include"
        })
        window.location.href = "/login"
    })
}