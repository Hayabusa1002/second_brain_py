import { createTransaction, updateTransaction } from "../api/transactions.js"

export function initEdit({ categories, accounts, onSaved }) {
    const editCard   = document.getElementById("edit-card")
    const editTitle  = document.getElementById("edit-card-title")
    const form       = document.getElementById("transaction-form")
    const transId    = document.getElementById("transaction-id")
    const typeSelect = document.getElementById("type-select")
    const catSelect  = document.getElementById("category-select")
    const accSelect  = document.getElementById("account-select")
    const editError  = document.getElementById("edit-error")

    // Populate account select
    accounts.forEach(a => {
        const opt = document.createElement("option")
        opt.value = a.id
        opt.textContent = `${a.name} (${a.type})`
        accSelect.appendChild(opt)
    })

    function renderCategories(type) {
        catSelect.innerHTML = categories
            .filter(c => c.type === type)
            .map(c => `<option value="${c.id}">${c.name}</option>`)
            .join("")
    }

    typeSelect.addEventListener("change", () => renderCategories(typeSelect.value))
    renderCategories(typeSelect.value)

    function openEdit(t) {
        editError.textContent = ""
        form.reset()
        renderCategories(t ? t.type : typeSelect.value)

        if (t) {
            editTitle.textContent  = "Edit transaction"
            transId.value          = t.id
            form.account_id.value  = t.account_id
            form.amount.value      = t.amount
            form.type.value        = t.type
            renderCategories(t.type)
            form.category_id.value = t.category_id
            form.date.value        = t.date
            form.description.value = t.description ?? ""
        } else {
            editTitle.textContent = "Add transaction"
            transId.value         = ""
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

        const isEdit = transId.value !== ""
        const data = {
            account_id:  form.account_id.value,
            amount:      parseFloat(form.amount.value),
            type:        form.type.value,
            category_id: form.category_id.value,
            date:        form.date.value,
            description: form.description.value || null,
        }

        try {
            if (isEdit) {
                await updateTransaction(transId.value, data)
            } else {
                await createTransaction(data)
            }
            hideEdit()
            await onSaved()
        } catch (err) {
            editError.textContent = err.message
        }
    })

    return { openEdit, hideEdit }
}