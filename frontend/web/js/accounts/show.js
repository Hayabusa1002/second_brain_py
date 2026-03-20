import { fetchWithAuth } from "../api/base.js"

export function initShow({ onEdit }) {
    const tbody       = document.getElementById("accounts-tbody")
    const tableWrapper = document.getElementById("table-wrapper")
    const emptyMsg    = document.getElementById("empty-msg")
    const rowTemplate = document.getElementById("row-template")

    function checkEmpty() {
        const hasRows = tbody.querySelector("tr")
        tableWrapper.style.display = hasRows ? "block" : "none"
        emptyMsg.style.display     = hasRows ? "none"  : "block"
    }

    function addRow(account) {
        const row = rowTemplate.content.cloneNode(true).querySelector("tr")
        row.id = `row-${account.id}`
        row.querySelector(".col-name").textContent      = account.name
        row.querySelector(".col-type span").textContent = account.type
        row.querySelector(".col-date").textContent      = new Date(account.created_at).toLocaleDateString()

        row.querySelector(".btn-edit").addEventListener("click",   () => onEdit(account))
        row.querySelector(".btn-delete").addEventListener("click", () => remove(account.id))

        tbody.appendChild(row)
    }

    async function loadAccounts() {
        tbody.innerHTML = ""
        const res = await fetchWithAuth("/api/accounts")
        if (!res) return
        const accounts = await res.json()
        accounts.forEach(addRow)
        checkEmpty()
    }

    async function remove(id) {
        if (!confirm("Delete this account?")) return
        const res = await fetchWithAuth(`/api/accounts/${id}`, { method: "DELETE" })
        if (res && res.ok) {
            document.getElementById(`row-${id}`).remove()
            checkEmpty()
        }
    }

    return { loadAccounts, addRow, checkEmpty }
}