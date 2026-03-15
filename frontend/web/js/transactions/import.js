import { requireAuth } from "../auth/guard.js";
import { importTransactions } from "../api/imports.js";

requireAuth();

document
    .getElementById("import-form")
    .addEventListener("submit", async (event) => {
        event.preventDefault();

        const file = document.getElementById("file-input").files[0];
        if (!file) return;

        try {
            const result = await importTransactions(file);
            renderResult(result);
        } catch (error) {
            console.error(error);
            alert(`Error: ${error.message}`);
        }
    });

function renderResult(result) {
    const section      = document.getElementById("result");
    const summary      = document.getElementById("result-summary");
    const errorSection = document.getElementById("error-section");
    const errorTbody   = document.querySelector("#error-table tbody");

    section.style.display = "block";
    summary.textContent   =
        `Total rows: ${result.total} | Imported: ${result.imported} | Errors: ${result.errors.length}`;

    errorTbody.innerHTML = "";

    if (result.errors.length > 0) {
        errorSection.style.display = "block";
        result.errors.forEach(e => {
            const row = document.createElement("tr");
            row.innerHTML = `<td>${e.row}</td><td>${e.error}</td>`;
            errorTbody.appendChild(row);
        });
    } else {
        errorSection.style.display = "none";
    }
}