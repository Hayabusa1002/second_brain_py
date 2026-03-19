export async function login(email, password) {
    const response = await fetch("/api/auth/login", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })

    const data = await response.json()

    if (!response.ok) {
        throw new Error(data.detail ?? "Login failed")
    }

    return data
}

export async function register(name, email, password) {
    const response = await fetch("/api/auth/register", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
    })

    const data = await response.json()

    if (!response.ok) {
        throw new Error(data.detail ?? "Registration failed")
    }

    return data
}