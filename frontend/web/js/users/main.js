import { requireAuth } from "../auth/guard.js"
import { initShow } from "./show.js"
import { initEdit } from "./edit.js"

await requireAuth()

const { openEdit } = initEdit({
  onSaved: (user, isEdit) => {
    if (isEdit) {
      const row = document.getElementById(`user-row-${user.id}`)
      if (row) {
        row.querySelector(".col-name").textContent = user.name
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
  onToggleBan: (u, row) => toggleBan(u, row),
  onDelete: (u, row) => deleteUser(u, row), 
})

async function toggleBan(user, row) {
  const btn = row.querySelector(".btn-toggle-ban")
  const isBanned = btn.textContent.trim() === "Unban"
  const action = isBanned ? "unban" : "ban"
  const msg = isBanned
    ? `Unban "${user.name}"? They will be able to log in again.`
    : `Ban "${user.name}"? They won't be able to log in.`

  if (!confirm(msg)) return

  const res = await fetch(`/api/users/${user.id}/${action}`, { method: "POST" })
  if (!res.ok) return

  const statusBadge = row.querySelector(".col-status span")
  if (isBanned) {
    statusBadge.textContent = "active"
    statusBadge.className = "badge bg-green-lt"
    btn.textContent = "Ban"
    btn.classList.replace("btn-warning", "btn-danger")
  } else {
    statusBadge.textContent = "banned"
    statusBadge.className = "badge bg-red-lt"
    btn.textContent = "Unban"
    btn.classList.replace("btn-danger", "btn-warning")
  }
}

async function deleteUser(user, row) {                                          // ← nuevo
  if (!confirm(`¿Eliminar a "${user.name}" y todas sus cuentas y transacciones?\nEsta acción no se puede deshacer.`)) return

  const res = await fetch(`/api/users/${user.id}`, { method: "DELETE" })

  if (res.status === 204) {
    row.remove()
    checkEmpty()
  } else {
    const err = await res.json().catch(() => ({}))
    alert(err.detail || "Error al eliminar usuario")
  }
}

document.getElementById("btn-add").addEventListener("click", () => openEdit(null))

await loadUsers()