import { importTransactions } from "../api/imports.js"

export function initImport({ onImported }) {
    const importCard   = document.getElementById("import-card")
    const importForm   = document.getElementById("import-form")
    const importResult = document.getElementById("import-result")
    const resultSummary = document.getElementById("result-summary")
    const errorSection = document.getElementById("error-section")
    const errorTable   = document.getElementById("error-table")

    document.getElementById("btn-import-cancel").addEventListener("click", () => {
        importCard.style.display  = "none"
        importResult.style.display = "none"
        importForm.reset()
    })

    importForm.addEventListener("submit", async (event) => {
        event.preventDefault()

        const file = document.getElementById("file-input").files[0]
        if (!file) return

        try {
            const result = await importTransactions(file)
            renderResult(result)
            await onImported()
        } catch (error) {
            console.error(error)
            alert(`Error: ${error.message}`)
        }
    })

    function renderResult(result) {
        importResult.style.display = "block"
        resultSummary.textContent  = `Total rows: ${result.total} | Imported: ${result.imported} | Errors: ${result.errors.length}`
        errorTable.innerHTML       = ""

        if (result.errors.length > 0) {
            errorSection.style.display = "block"
            result.errors.forEach(e => {
                const row = document.createElement("tr")
                row.innerHTML = `<td>${e.row}</td><td>${e.error}</td>`
                errorTable.appendChild(row)
            })
        } else {
            errorSection.style.display = "none"
        }
    }
}