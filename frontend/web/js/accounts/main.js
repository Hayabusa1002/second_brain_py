import { requireAuth } from "../auth/guard.js"
import { initShow }    from "./show.js"
import { initEdit }    from "./edit.js"

await requireAuth()

const { openEdit, hideEdit } = initEdit({
    onSaved: async (account, isEdit) => {
        if (isEdit) {
            const row = document.getElementById(`row-${account.id}`)
            row.querySelector(".col-name").textContent      = account.name
            row.querySelector(".col-type span").textContent = account.type
        } else {
            addRow(account)
            checkEmpty()
        }
    }
})

const { loadAccounts, addRow, checkEmpty } = initShow({ onEdit: (a) => openEdit(a) })

document.getElementById("btn-add").addEventListener("click", () => openEdit(null))

await loadAccounts()