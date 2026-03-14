const TOKEN_KEY = "sb_token"

export function getToken() {
    return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
    localStorage.setItem(TOKEN_KEY, token)
}

export function removeToken() {
    localStorage.removeItem(TOKEN_KEY)
}

export function requireAuth() {
    if (!getToken()) {
        window.location.href = "/login"
    }
}

export function logout() {
    removeToken()
    window.location.href = "/login"
}