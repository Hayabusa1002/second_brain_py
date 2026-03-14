import { getToken, removeToken } from "../auth/guard.js"

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