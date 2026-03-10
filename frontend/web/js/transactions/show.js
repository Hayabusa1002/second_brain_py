async function loadExpenses() {
  const response = await fetch("/transactions")
  const data = await response.json()
  const table = document.querySelector("#expenses-table tbody")

  data.forEach(tx => {
    const row = document.createElement("tr")

    row.innerHTML = `
      <td>${tx.date}</td>
      <td>${tx.category_id}</td>
      <td>${tx.amount}</td>
    `

    table.appendChild(row)
  })
}

loadExpenses()