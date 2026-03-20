import { requireAuth } from "../auth/guard.js"
import { initShow }   from "./show.js"
import { initEdit }   from "./edit.js"
import { initOwners } from "./owners.js"

await requireAuth()

const { openEdit } = initEdit({
    onSaved: (account, isEdit) => {
        if (isEdit) {
            const row = document.getElementById(`row-${account.id}`)
            row.querySelector(".col-name").textContent        = account.name
            row.querySelector(".col-type span").textContent   = account.type
        } else {
            account.owners = []
            addRow(account)
            checkEmpty()
        }
    }
})

const { open: openOwners } = initOwners({
    onUpdated: (account) => {
        const row = document.getElementById(`row-${account.id}`)
        if (row) {
            row.querySelector(".col-owners").textContent =
                account.owners.map(o => o.name).join(", ") || "—"
        }
    }
})

const { loadAccounts, addRow, checkEmpty } = initShow({
    onEdit:         (a) => openEdit(a),
    onManageOwners: (a) => openOwners(a),
})

document.getElementById("btn-add").addEventListener("click", () => openEdit(null))

await loadAccounts()