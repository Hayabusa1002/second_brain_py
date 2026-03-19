import { fetchWithAuth } from "../api/base.js"
import { requireAuth } from "../auth/guard.js"

await requireAuth()

const tbody       = document.getElementById("accounts-tbody")
const tableWrapper = document.getElementById("table-wrapper")
const emptyMsg    = document.getElementById("empty-msg")
const rowTemplate = document.getElementById("row-template")
const formCard    = document.getElementById("form-card")
const formTitle   = document.getElementById("form-title")
const form        = document.getElementById("account-form")
const fieldName   = document.getElementById("field-name")
const fieldType   = document.getElementById("field-type")
const accountId   = document.getElementById("account-id")
const formError   = document.getElementById("form-error")

function checkEmpty() {
    const hasRows = tbody.querySelector("tr")
    tableWrapper.style.display = hasRows ? "block" : "none"
    emptyMsg.style.display     = hasRows ? "none"  : "block"
}

function addRow(account) {
    const row = rowTemplate.content.cloneNode(true).querySelector("tr")
    row.id = `row-${account.id}`
    row.querySelector(".col-name").textContent       = account.name
    row.querySelector(".col-type span").textContent  = account.type
    row.querySelector(".col-date").textContent       = new Date(account.created_at).toLocaleDateString()

    row.querySelector(".btn-edit").addEventListener("click",   () => openEdit(account))
    row.querySelector(".btn-delete").addEventListener("click", () => deleteAccount(account.id))

    tbody.appendChild(row)
}

function showForm(title, name = "", type = "individual", id = "") {
    formTitle.textContent  = title
    fieldName.value        = name
    fieldType.value        = type
    accountId.value        = id
    formError.textContent  = ""
    formCard.style.display = "block"
    fieldName.focus()
}

function hideForm() {
    formCard.style.display = "none"
    form.reset()
}

async function load() {
    const res = await fetchWithAuth("/api/accounts")
    if (!res) return
    const accounts = await res.json()
    accounts.forEach(addRow)
    checkEmpty()
}

document.getElementById("btn-new").addEventListener("click", () => {
    showForm("New account")
})

document.getElementById("btn-cancel").addEventListener("click", hideForm)

form.addEventListener("submit", async (e) => {
    e.preventDefault()
    formError.textContent = ""

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
        formError.textContent = data.detail ?? "Error saving account."
        return
    }

    if (isEdit) {
        const row = document.getElementById(`row-${accountId.value}`)
        row.querySelector(".col-name").textContent      = data.name
        row.querySelector(".col-type span").textContent = data.type
    } else {
        addRow(data)
        checkEmpty()
    }

    hideForm()
})

function openEdit(account) {
    showForm("Edit account", account.name, account.type, account.id)
}

async function deleteAccount(id) {
    if (!confirm("Delete this account?")) return

    const res = await fetchWithAuth(`/api/accounts/${id}`, { method: "DELETE" })
    if (res && res.ok) {
        document.getElementById(`row-${id}`).remove()
        checkEmpty()
    }
}

load()