import { getToken, removeToken, logout } from "../auth/guard.js"

export async function fetchWithAuth(url, options = {}) {
    const token   = getToken()
    const headers = { ...options.headers }

    if (token) {
        headers["Authorization"] = `Bearer ${token}`
    }

    const response = await fetch(url, { ...options, headers })

    if (response.status === 401) {
        removeToken()
        window.location.href = "/login"
        return null
    }

    return response
}

const logoutBtn = document.getElementById("btn-logout")
if (logoutBtn) {
    logoutBtn.addEventListener("click", logout)
}