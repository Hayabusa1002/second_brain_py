import { getTransactions } from "../api/transactions.js"

async function loadTransactions() {
  try {
    const transactions = await getTransactions()
    const table = document.querySelector("#transactions-table")

    transactions.forEach(t => {
      const row = document.createElement("tr")

      row.innerHTML = `
        <td>${t.date}</td>
        <td>${t.amount}</td>
        <td>${t.type}</td>
      `

      table.appendChild(row)
    })
  } catch (error) {
    console.error(error)
  }
}

loadTransactions()