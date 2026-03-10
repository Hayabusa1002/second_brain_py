export async function getTransactions() {

    const response = await fetch("/transactions")

    if (!response.ok) {
        throw new Error("Error fetching transactions")
    }

    return await response.json()
}

export async function createTransaction(data) {

    const response = await fetch("/transactions", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })

    if (!response.ok) {
        throw new Error("Error creating transaction")
    }

    return await response.json()
}