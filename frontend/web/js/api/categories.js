export async function getCategories() {
    const response = await fetch("/categories")

    if (!response.ok) {
        throw new Error("Error fetching categories")
    }

    return await response.json()
}