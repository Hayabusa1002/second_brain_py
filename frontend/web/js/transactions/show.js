import { getTransactions, deleteTransaction } from "../api/transactions.js"

export function initShow({ categoryMap, accountMap, onEdit }) {
    const tbody       = document.querySelector("#transactions-table tbody")
    const rowTemplate = document.getElementById("row-template")

    function addRow(t) {
        const row = rowTemplate.content.cloneNode(true).querySelector("tr")
        row.id = `row-${t.id}`
        row.querySelector(".col-date").textContent        = t.date
        row.querySelector(".col-account").textContent     = accountMap[t.account_id]   ?? "-"
        row.querySelector(".col-type").textContent        = t.type
        row.querySelector(".col-category").textContent    = categoryMap[t.category_id] ?? "-"
        row.querySelector(".col-amount").textContent      = t.amount
        row.querySelector(".col-description").textContent = t.description ?? ""

        row.querySelector(".btn-edit").addEventListener("click",   () => onEdit(t))
        row.querySelector(".btn-delete").addEventListener("click", () => remove(t.id))
        tbody.appendChild(row)
    }

    async function loadTransactions(filters = {}) {
        tbody.innerHTML = ""
        const transactions = await getTransactions(filters)
        transactions.forEach(addRow)
    }

    async function remove(id) {
        if (!confirm("Delete this transaction?")) return
        await deleteTransaction(id)
        document.getElementById(`row-${id}`).remove()
    }

    function getFilters() {
        return {
            account_id:  document.getElementById("filter-account").value  || undefined,
            type:        document.getElementById("filter-type").value     || undefined,
            category_id: document.getElementById("filter-category").value || undefined,
        }
    }

    document.getElementById("btn-filter").addEventListener("click", () => loadTransactions(getFilters()))
    document.getElementById("btn-clear").addEventListener("click", () => {
        document.getElementById("filter-account").value  = ""
        document.getElementById("filter-type").value    = ""
        document.getElementById("filter-category").value = ""
        loadTransactions()
    })

    return { loadTransactions }
}