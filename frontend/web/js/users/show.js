import { fetchWithAuth } from "../api/base.js"

export function initShow({ onEdit, onToggleBan }) {
  const tbody = document.getElementById("users-tbody")
  const tableWrapper = document.getElementById("users-table-wrapper")
  const emptyMsg = document.getElementById("users-empty-msg")
  const rowTemplate = document.getElementById("user-row-template")

  const STATUS_CLASS = {
    active: "bg-green-lt",
    pending: "bg-yellow-lt",
    inactive: "bg-secondary-lt",
    banned: "bg-red-lt",
  }

  const ROLE_CLASS = {
    admin: "bg-purple-lt",
    owner: "bg-blue-lt",
    partner: "bg-azure-lt",
  }

  function checkEmpty() {
    const hasRows = tbody.querySelector("tr")
    tableWrapper.style.display = hasRows ? "block" : "none"
    emptyMsg.style.display = hasRows ? "none" : "block"
  }

  function addRow(user) {
    const row = rowTemplate.content.cloneNode(true).querySelector("tr")
    row.id = `user-row-${user.id}`
    row.querySelector(".col-name").textContent = user.name
    row.querySelector(".col-email").textContent = user.email
    row.querySelector(".col-date").textContent =
      new Date(user.created_at).toLocaleDateString()

    const roleBadge = row.querySelector(".col-role span")
    roleBadge.textContent = user.role
    roleBadge.className = `badge ${ROLE_CLASS[user.role] ?? "bg-secondary-lt"}`

    const statusBadge = row.querySelector(".col-status span")
    statusBadge.textContent = user.status
    statusBadge.className = `badge ${STATUS_CLASS[user.status] ?? "bg-secondary-lt"}`

    const btnToggleBan = row.querySelector(".btn-toggle-ban")
    if (user.status === "banned") {
      btnToggleBan.textContent = "Unban"
      btnToggleBan.classList.add("btn-warning")
    } else {
      btnToggleBan.textContent = "Ban"
      btnToggleBan.classList.add("btn-danger")
    }

    btnToggleBan.addEventListener("click", () => onToggleBan(user, row))
    row.querySelector(".btn-edit").addEventListener("click", () => onEdit(user))
    tbody.appendChild(row)
  }

  async function loadUsers() {
    tbody.innerHTML = ""
    const res = await fetchWithAuth("/api/users")
    if (!res || !res.ok) return
    const data = await res.json()
    data.users.forEach(addRow)
    checkEmpty()
  }

  return { loadUsers, addRow, checkEmpty }
}