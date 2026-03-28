import { requireAuth } from "../auth/guard.js"
import { getCategories } from "../api/categories.js"
import { getAccounts } from "../api/accounts.js"
import { initShow } from "./show.js"
import { initEdit } from "./edit.js"
import { initImport } from "./import.js"
import { exportCsv, exportJson, exportXlsx, exportPdf } from "../api/export.js"

await requireAuth()

// Load shared data and pass it to each module
const [categories, accounts] = await Promise.all([getCategories(), getAccounts()])

const categoryMap = Object.fromEntries(categories.map(c => [c.id, c.name]))
const accountMap  = Object.fromEntries(accounts.map(a  => [a.id, a.name]))

// Populate filter selects (owned by show.js DOM)
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

// Init edit first, get openEdit
const { openEdit, hideEdit } = initEdit({ categories, accounts, onSaved: () => loadTransactions() })

// Then init show passing openEdit already resolved
const { loadTransactions, getFilters: getActiveFilters } = initShow({ categoryMap, accountMap, onEdit: (t) => openEdit(t) })

initImport({ onImported: () => loadTransactions() })

document.getElementById("btn-add").addEventListener("click", () => {
    document.getElementById("import-card").style.display = "none"
    openEdit(null)
})

document.getElementById("btn-import").addEventListener("click", () => {
    hideEdit()
    document.getElementById("import-card").style.display = "block"
    document.getElementById("import-card").scrollIntoView({ behavior: "smooth" })
})

// Export buttons
document.getElementById("export-csv").addEventListener("click", (e) => {
    e.preventDefault()
    exportCsv(getActiveFilters())
})

document.getElementById("export-json").addEventListener("click", (e) => {
    e.preventDefault()
    exportJson(getActiveFilters())
})

document.getElementById("export-xlsx").addEventListener("click", (e) => {
    e.preventDefault()
    exportXlsx(getActiveFilters())
})

document.getElementById("export-pdf").addEventListener("click", (e) => {
    e.preventDefault()
    exportPdf(getActiveFilters())
})

await loadTransactions()