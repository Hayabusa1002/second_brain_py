import { fetchWithAuth } from "../api/base.js"

export function initEdit({ onSaved }) {
    const editCard   = document.getElementById("user-edit-card")
    const editTitle  = document.getElementById("user-edit-card-title")
    const form       = document.getElementById("user-form")
    const userId     = document.getElementById("user-id")
    const fieldName  = document.getElementById("user-field-name")
    const fieldEmail = document.getElementById("user-field-email")
    const fieldPass  = document.getElementById("user-field-password")
    const fieldRole  = document.getElementById("user-field-role")
    const passHint   = document.getElementById("user-password-hint")
    const editError  = document.getElementById("user-edit-error")

    function openEdit(user) {
        editError.textContent = ""
        form.reset()

        if (user) {
            editTitle.textContent = "Edit user"
            userId.value          = user.id
            fieldName.value       = user.name
            fieldEmail.value      = user.email
            fieldRole.value       = user.role
            fieldEmail.disabled   = true
            fieldPass.required    = false
            passHint.textContent  = "Leave blank to keep current password"
        } else {
            editTitle.textContent = "New user"
            userId.value          = ""
            fieldEmail.disabled   = false
            fieldPass.required    = true
            passHint.textContent  = ""
        }

        editCard.style.display = "block"
        editCard.scrollIntoView({ behavior: "smooth" })
    }

    function hideEdit() {
        editCard.style.display = "none"
        fieldEmail.disabled    = false
        form.reset()
    }

    document.getElementById("btn-user-edit-cancel").addEventListener("click", hideEdit)

    form.addEventListener("submit", async (e) => {
        e.preventDefault()
        editError.textContent = ""

        const isEdit = userId.value !== ""

        const url    = isEdit ? `/api/users/${userId.value}` : "/api/users"
        const method = isEdit ? "PUT" : "POST"
        const body   = isEdit
            ? { name: fieldName.value, role: fieldRole.value }
            : {
                name:     fieldName.value,
                email:    fieldEmail.value,
                password: fieldPass.value,
                role:     fieldRole.value,
              }

        const res = await fetchWithAuth(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        })

        if (!res) return
        const data = await res.json()

        if (!res.ok) {
            editError.textContent = data.detail ?? "Error saving user."
            return
        }

        hideEdit()
        onSaved(data.user, isEdit)
    })

    return { openEdit, hideEdit }
}