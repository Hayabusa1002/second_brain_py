export async function isAuthenticated() {
    try {
        const res = await fetch("/api/auth/me", { credentials: "include" })
        return res.ok
    } catch {
        return false
    }
}

export async function requireAuth() {
    if (!(await isAuthenticated())) {
        window.location.href = "/login"
    }
}

export async function logout() {
    await fetch("/api/auth/logout", { method: "POST", credentials: "include" })
    window.location.href = "/login"
}