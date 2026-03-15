const TOKEN_KEY = "sb_token"


export function getToken() {
    return localStorage.getItem(TOKEN_KEY)
}


export function setToken(token) {
    localStorage.setItem(TOKEN_KEY, token)
    document.cookie = `access_token=${token}; path=/; SameSite=Strict`
}


export function removeToken() {
    localStorage.removeItem(TOKEN_KEY)
    document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT"
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