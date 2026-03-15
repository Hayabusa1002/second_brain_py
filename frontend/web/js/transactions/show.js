import { requireAuth } from "../auth/guard.js"
import { getTransactions } from "../api/transactions.js"
import { getCategories } from "../api/categories.js"
import { getAccounts } from "../api/accounts.js"

requireAuth()

let categoryMap = {}
let accountMap  = {}

async function loadFiltersData() {
    const [categories, accounts] = await Promise.all([getCategories(), getAccounts()])

    categoryMap = Object.fromEntries(categories.map(c => [c.id, c.name]))
    accountMap  = Object.fromEntries(accounts.map(a => [a.id, a.name]))

    const filterCategory = document.getElementById("filter-category")
    categories.forEach(c => {
        const opt = document.createElement("option")
        opt.value = c.id
        opt.textContent = c.name
        filterCategory.appendChild(opt)
    })

    const filterAccount = document.getElementById("filter-account")
    accounts.forEach(a => {
        const opt = document.createElement("option")
        opt.value = a.id
        opt.textContent = `${a.name} (${a.type})`
        filterAccount.appendChild(opt)
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
            <td>${accountMap[t.account_id]  ?? "-"}</td>
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
        account_id:  document.getElementById("filter-account").value  || undefined,
        type:        document.getElementById("filter-type").value     || undefined,
        category_id: document.getElementById("filter-category").value || undefined,
    }
}

document.getElementById("btn-filter")
    .addEventListener("click", () => loadTransactions(getFilters()))

document.getElementById("btn-clear")
    .addEventListener("click", () => {
        document.getElementById("filter-account").value  = ""
        document.getElementById("filter-type").value     = ""
        document.getElementById("filter-category").value = ""
        loadTransactions()
    })

async function init() {
    await loadFiltersData()
    loadTransactions()
}

init()