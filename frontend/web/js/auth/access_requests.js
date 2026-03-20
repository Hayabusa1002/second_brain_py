import { fetchWithAuth } from "../api/base.js"
import { requireAuth } from "./guard.js"

await requireAuth()

const tbody       = document.getElementById("users-tbody")
const tableWrapper = document.getElementById("table-wrapper")
const emptyMsg    = document.getElementById("empty-msg")
const rowTemplate = document.getElementById("row-template")

function checkEmpty() {
    if (!tbody.querySelector("tr")) {
        tableWrapper.style.display = "none"
        emptyMsg.style.display = "block"
    }
}

function addRow(user) {
    const row = rowTemplate.content.cloneNode(true).querySelector("tr")
    row.id = `row-${user.id}`
    row.querySelector(".col-name").textContent  = user.name
    row.querySelector(".col-email").textContent = user.email
    row.querySelector(".col-role span").textContent = user.role
    row.querySelector(".col-date").textContent  = new Date(user.created_at).toLocaleDateString()

    row.querySelector(".btn-approve").addEventListener("click", () => action(user.id, "approve"))
    row.querySelector(".btn-reject").addEventListener("click",  () => action(user.id, "reject"))

    tbody.appendChild(row)
}

async function action(id, type) {
    const res = await fetchWithAuth(`/api/users/${id}/${type}`, { method: "POST" })
    if (res && res.ok) {
        document.getElementById(`row-${id}`).remove()
        checkEmpty()
    }
}

async function load() {
    const res = await fetchWithAuth("/api/users/pending")
    if (!res) return

    const data = await res.json()
    const users = data.users ?? data
    if (!users || !users.length) {
        checkEmpty()
        return
    }

    users.forEach(addRow)
}

load()