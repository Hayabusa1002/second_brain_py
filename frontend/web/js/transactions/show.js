import { getTransactions } from "../api/transactions.js"

async function loadTransactions() {
  try {
    const transactions = await getTransactions()
    const tbody = document.querySelector("#transactions-table tbody")

    transactions.forEach(t => {
      const row = document.createElement("tr")

      row.innerHTML = `
        <td>${t.date}</td>
        <td>${t.type}</td>
        <td>${t.amount}</td>
        <td>${t.description ?? ""}</td>
      `

      tbody.appendChild(row)
    })
  } catch (error) {
    console.error(error)
  }
}

loadTransactions()