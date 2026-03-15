import { fetchWithAuth } from "./base.js";

export async function getAccounts() {
    const response = await fetchWithAuth("/accounts");
    if (!response) return [];
    if (!response.ok) throw new Error("Error fetching accounts");
    return await response.json();
}