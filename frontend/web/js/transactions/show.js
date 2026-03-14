import { getTransactions } from "../api/transactions.js"
import { getCategories } from "../api/categories.js"

let categoryMap = {}

async function loadCategories() {
    const categories = await getCategories()
    categoryMap = Object.fromEntries(categories.map(c => [c.id, c.name]))

    const filterCategory = document.getElementById("filter-category")
    categories.forEach(c => {
        const option = document.createElement("option")
        option.value       = c.id
        option.textContent = c.name
        filterCategory.appendChild(option)
    })
}

async function loadTransactions(filters = {}) {
    const tbody = document.querySelector("#transactions-table tbody")
    tbody.innerHTML = ""

    const transactions = await getTransactions(filters)

    transactions.forEach(t => {
        const row = document.createElement("tr")
        row.innerHTML = `
            <td>${t.date}</td>
            <td>${t.type}</td>
            <td>${categoryMap[t.category_id] ?? "-"}</td>
            <td>${t.amount}</td>
            <td>${t.description ?? ""}</td>
        `
        tbody.appendChild(row)
    })
}

function getFilters() {
    return {
        type:        document.getElementById("filter-type").value    || undefined,
        category_id: document.getElementById("filter-category").value || undefined,
    }
}

document.getElementById("btn-filter").addEventListener("click", () => loadTransactions(getFilters()))

document.getElementById("btn-clear").addEventListener("click", () => {
    document.getElementById("filter-type").value     = ""
    document.getElementById("filter-category").value = ""
    loadTransactions()
})

async function init() {
    await loadCategories()
    loadTransactions()
}

init()