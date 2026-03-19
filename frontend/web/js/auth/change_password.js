import { fetchWithAuth } from "../api/base.js"
import { requireAuth } from "./guard.js"

await requireAuth()

document
    .getElementById("change-password-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault()

        const form = event.target
        const errorMsg   = document.getElementById("error-msg")
        const successMsg = document.getElementById("success-msg")

        errorMsg.textContent = ""
        successMsg.style.display = "none"

        if (form.new_password.value !== form.confirm_password.value) {
            errorMsg.textContent = "New passwords do not match."
            return
        }

        const res = await fetchWithAuth("/api/auth/password", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                current_password: form.current_password.value,
                new_password:     form.new_password.value,
            }),
        })

        if (!res) return

        const data = await res.json()

        if (!res.ok) {
            errorMsg.textContent = data.detail ?? "Error updating password."
            return
        }

        form.reset()
        successMsg.style.display = "block"
    })