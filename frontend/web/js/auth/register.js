import { register } from "../api/auth.js"
import { isAuthenticated } from "./guard.js"

if (await isAuthenticated()) {
    window.location.href = "/"
}

document
    .getElementById("register-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault()

        const form = event.target

        try {
            await register(form.name.value, form.email.value, form.password.value)
            form.style.display = "none"
            document.getElementById("pending-msg").style.display = "block"
        } catch (error) {
            document.getElementById("error-msg").textContent = error.message
        }
    })