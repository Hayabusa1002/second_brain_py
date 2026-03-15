import { requireAuth } from "../auth/guard.js"
import { createTransaction } from "../api/transactions.js"
import { getCategories } from "../api/categories.js"
import { getAccounts } from "../api/accounts.js"

requireAuth()

const typeSelect     = document.getElementById("type-select")
const categorySelect = document.getElementById("category-select")
const accountSelect  = document.getElementById("account-select")

let allCategories = []

function renderCategories(type) {
    const filtered = allCategories.filter(c => c.type === type)
    categorySelect.innerHTML = filtered
        .map(c => `<option value="${c.id}">${c.name}</option>`)
        .join("")
}

async function init() {
    const [categories, accounts] = await Promise.all([getCategories(), getAccounts()])

    allCategories = categories
    renderCategories(typeSelect.value)

    accountSelect.innerHTML = accounts
        .map(a => `<option value="${a.id}">${a.name} (${a.type})</option>`)
        .join("")
}

typeSelect.addEventListener("change", () => renderCategories(typeSelect.value))

document
    .getElementById("transaction-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault()

        const form = event.target
        const data = {
            account_id:  form.account_id.value,
            amount:      parseFloat(form.amount.value),
            type:        form.type.value,
            date:        form.date.value,
            description: form.description.value || null,
            category_id: form.category_id.value,
        }

        try {
            await createTransaction(data)
            alert("Transaction saved")
            form.reset()
            renderCategories(typeSelect.value)
        } catch (error) {
            console.error(error)
            alert("Error saving transaction")
        }
    })

init()