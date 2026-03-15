import { fetchWithAuth } from "./base.js"

export async function getCategories() {
    const response = await fetchWithAuth("/api/categories")
    if (!response) return []
    if (!response.ok) throw new Error("Error fetching categories")
    return await response.json()
}