import { fetchWithAuth } from "./base.js";

export async function importTransactions(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetchWithAuth("/transactions/import", {
        method: "POST",
        body: formData,
    });

    if (!response) return null;
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail ?? "Error importing file");
    return result;
}