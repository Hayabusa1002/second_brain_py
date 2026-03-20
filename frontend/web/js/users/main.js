import { requireAuth } from "../auth/guard.js"
import { initShow }    from "./show.js"
import { initEdit }    from "./edit.js"

await requireAuth()

const { openEdit } = initEdit({
    onSaved: (user, isEdit) => {
        if (isEdit) {
            const row = document.getElementById(`user-row-${user.id}`)
            if (row) {
                row.querySelector(".col-name").textContent  = user.name
                row.querySelector(".col-email").textContent = user.email
                row.querySelector(".col-role span").textContent = user.role
            }
        } else {
            addRow(user)
            checkEmpty()
        }
    }
})

const { loadUsers, addRow, checkEmpty } = initShow({
    onEdit: (u) => openEdit(u),
    onBan:  (u) => confirmBan(u),
})

async function confirmBan(user) {
    if (!confirm(`Ban user "${user.name}"? They won't be able to log in.`)) return
    const res = await fetch(`/api/users/${user.id}/ban`, { method: "POST" })
    if (!res.ok) return
    const row = document.getElementById(`user-row-${user.id}`)
    if (row) {
        row.querySelector(".col-status span").textContent  = "banned"
        row.querySelector(".col-status span").className   = "badge bg-red-lt"
        row.querySelector(".btn-ban").disabled = true
    }
}

document.getElementById("btn-add").addEventListener("click", () => openEdit(null))

await loadUsers()