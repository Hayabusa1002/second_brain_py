import { createTransaction } from "../api/transactions.js"
import { getCategories } from "../api/categories.js"

const typeSelect     = document.getElementById("type-select")
const categorySelect = document.getElementById("category-select")

let allCategories = []

function renderCategories(type) {
    const filtered = allCategories.filter(c => c.type === type)
    categorySelect.innerHTML = filtered
        .map(c => `<option value="${c.id}">${c.name}</option>`)
        .join("")
}

async function init() {
    allCategories = await getCategories()
    renderCategories(typeSelect.value)
}

typeSelect.addEventListener("change", () => renderCategories(typeSelect.value))

document
    .getElementById("transaction-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault()

        const form = event.target
        const data = {
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