export async function getTransactions(filters = {}) {
    const params = new URLSearchParams()
    if (filters.type)        params.append("type", filters.type)
    if (filters.category_id) params.append("category_id", filters.category_id)

    const query = params.toString()
    const url   = query ? `/transactions?${query}` : "/transactions"

    const response = await fetch(url)
    if (!response.ok) {
        throw new Error("Error fetching transactions")
    }

    return await response.json()
}

export async function createTransaction(data) {
    const response = await fetch("/transactions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })

    if (!response.ok) {
        throw new Error("Error creating transaction")
    }

    return await response.json()
}