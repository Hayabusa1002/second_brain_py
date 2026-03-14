import { register } from "../api/auth.js"
import { setToken, getToken } from "./guard.js"

if (getToken()) {
    window.location.href = "/"
}

document
    .getElementById("register-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault()

        const form = event.target

        try {
            const data = await register(form.name.value, form.email.value, form.password.value)
            setToken(data.access_token)
            window.location.href = "/"
        } catch (error) {
            document.getElementById("error-msg").textContent = error.message
        }
    })