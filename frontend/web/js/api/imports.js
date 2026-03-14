export async function importTransactions(file) {
    const formData = new FormData()
    formData.append("file", file)

    const response = await fetch("/transactions/import", {
        method: "POST",
        body: formData,
    })

    const result = await response.json()

    if (!response.ok) {
        throw new Error(result.detail ?? "Error importing file")
    }

    return result
}