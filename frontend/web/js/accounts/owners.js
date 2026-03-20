import { fetchWithAuth } from "../api/base.js"

export function initOwners({ onUpdated }) {
    const card             = document.getElementById("owners-card")
    const title            = document.getElementById("owners-card-title")
    const accountId        = document.getElementById("owners-account-id")
    const select           = document.getElementById("owners-user-select")
    const list             = document.getElementById("owners-list")
    const emptyMsg         = document.getElementById("owners-empty")
    const btnAssign        = document.getElementById("btn-assign-owner")
    const btnCancel        = document.getElementById("btn-owners-cancel")
    const rowTemplate      = document.getElementById("owner-row-template")
    const defaultOptTpl    = document.getElementById("owner-select-default-template")
    const optionTpl        = document.getElementById("owner-select-option-template")

    let currentAccount = null

    btnCancel.addEventListener("click", hide)
    btnAssign.addEventListener("click", assign)

    async function open(account) {
        currentAccount = account
        accountId.value = account.id
        title.textContent = `Owners — ${account.name}`
        card.style.display = "block"
        card.scrollIntoView({ behavior: "smooth" })

        const isIndividual = account.type === "individual"
        btnAssign.style.display  = isIndividual ? "none" : ""
        select.style.display     = isIndividual ? "none" : ""

        if (!isIndividual) {
            await loadUsers()
        }

        renderOwners(account.owners, isIndividual)
    }

    function hide() {
        card.style.display = "none"
        currentAccount = null
        list.innerHTML = ""
        resetSelect()
    }

    function resetSelect() {
        select.innerHTML = ""
        const defaultOpt = defaultOptTpl.content.cloneNode(true)
        select.appendChild(defaultOpt)
    }

    async function loadUsers() {
        const res = await fetchWithAuth("/api/accounts/users/active")
        if (!res || !res.ok) return
        const data = await res.json()
        resetSelect()
        data.users.forEach(u => {
            const opt = optionTpl.content.cloneNode(true).querySelector("option")
            opt.value = u.id
            opt.textContent = u.name
            select.appendChild(opt)
        })
    }

    function addOwnerRow(owner, isIndividual = false) {
        const fragment = rowTemplate.content.cloneNode(true)
        const row = fragment.querySelector("div")
        row.id = `owner-row-${owner.id}`
        row.querySelector(".owner-name").textContent = owner.name

        const btnRemove = row.querySelector(".btn-remove-owner")
        if (isIndividual) {
            btnRemove.style.display = "none"
        } else {
            btnRemove.addEventListener("click", () => remove(owner.id))
        }

        list.appendChild(fragment)
    }

    function renderOwners(owners, isIndividual = false) {
        list.innerHTML = ""
        if (!owners || !owners.length) {
            emptyMsg.style.display = "block"
            return
        }
        emptyMsg.style.display = "none"
        owners.forEach(o => addOwnerRow(o, isIndividual))
    }

    async function assign() {
        const userId = select.value
        if (!userId || !currentAccount) return

        const res = await fetchWithAuth(
            `/api/accounts/${currentAccount.id}/owners/${userId}`,
            { method: "POST" }
        )
        if (!res || !res.ok) return

        const owner = { id: userId, name: select.options[select.selectedIndex].textContent }
        currentAccount.owners = currentAccount.owners || []
        currentAccount.owners.push(owner)
        addOwnerRow(owner)
        emptyMsg.style.display = "none"
        resetSelect()
        if (onUpdated) onUpdated(currentAccount)
    }

    async function remove(userId) {
        if (!currentAccount) return

        const res = await fetchWithAuth(
            `/api/accounts/${currentAccount.id}/owners/${userId}`,
            { method: "DELETE" }
        )
        if (!res || !res.ok) return

        currentAccount.owners = currentAccount.owners.filter(o => o.id !== userId)
        document.getElementById(`owner-row-${userId}`)?.remove()
        if (!currentAccount.owners.length) {
            emptyMsg.style.display = "block"
        }
        if (onUpdated) onUpdated(currentAccount)
    }

    return { open, hide }
}