import { fetchWithAuth } from "../api/base.js"

export function initEdit({ onSaved }) {
    const editCard  = document.getElementById("edit-card")
    const editTitle = document.getElementById("edit-card-title")
    const form      = document.getElementById("account-form")
    const accountId = document.getElementById("account-id")
    const fieldName = document.getElementById("field-name")
    const fieldType = document.getElementById("field-type")
    const editError = document.getElementById("edit-error")

    function openEdit(account) {
        editError.textContent = ""
        form.reset()

        if (account) {
            editTitle.textContent = "Edit account"
            accountId.value       = account.id
            fieldName.value       = account.name
            fieldType.value       = account.type
        } else {
            editTitle.textContent = "New account"
            accountId.value       = ""
        }

        editCard.style.display = "block"
        editCard.scrollIntoView({ behavior: "smooth" })
    }

    function hideEdit() {
        editCard.style.display = "none"
        form.reset()
    }

    document.getElementById("btn-edit-cancel").addEventListener("click", hideEdit)

    form.addEventListener("submit", async (e) => {
        e.preventDefault()
        editError.textContent = ""

        const isEdit  = accountId.value !== ""
        const url     = isEdit ? `/api/accounts/${accountId.value}` : "/api/accounts"
        const method  = isEdit ? "PUT" : "POST"

        const res = await fetchWithAuth(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: fieldName.value, type: fieldType.value }),
        })

        if (!res) return
        const data = await res.json()

        if (!res.ok) {
            editError.textContent = data.detail ?? "Error saving account."
            return
        }

        hideEdit()
        await onSaved(data, isEdit)
    })

    return { openEdit, hideEdit }
}