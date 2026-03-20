import { fetchWithAuth } from "./base.js"

export async function getTransactions(filters = {}) {
    const params = new URLSearchParams()
    if (filters.type)        params.append("type",        filters.type)
    if (filters.category_id) params.append("category_id", filters.category_id)
    if (filters.account_id)  params.append("account_id",  filters.account_id)

    const query    = params.toString()
    const url      = query ? `/api/transactions?${query}` : "/api/transactions"
    const response = await fetchWithAuth(url)
    if (!response) return []
    if (!response.ok) throw new Error("Error fetching transactions")
    return await response.json()
}

export async function createTransaction(data) {
    const response = await fetchWithAuth("/api/transactions", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify(data),
    })
    if (!response) return null
    if (!response.ok) throw new Error("Error creating transaction")
    return await response.json()
}

export async function updateTransaction(id, data) {
    const response = await fetchWithAuth(`/api/transactions/${id}`, {
        method:  "PUT",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify(data),
    })
    if (!response) return null
    if (!response.ok) throw new Error("Error updating transaction")
    return await response.json()
}

export async function deleteTransaction(id) {
    const response = await fetchWithAuth(`/api/transactions/${id}`, {
        method: "DELETE",
    })
    if (!response) return false
    if (!response.ok) throw new Error("Error deleting transaction")
    return true
}