import { login } from "../api/auth.js"
import { isAuthenticated } from "./guard.js"

if (await isAuthenticated()) {
    window.location.href = "/"
}

document
    .getElementById("login-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault()

        const form = event.target

        try {
            await login(form.email.value, form.password.value)
            window.location.href = "/"
        } catch (error) {
            const msg = error.message === "Pending request"
                ? "Your account is pending approval by an administrator."
                : error.message
            document.getElementById("error-msg").textContent = msg
        }
    })