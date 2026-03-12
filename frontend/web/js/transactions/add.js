import { createTransaction } from "../api/transactions.js"

document
  .getElementById("transaction-form")
  .addEventListener("submit", async (event) => {

    event.preventDefault()

    const form = event.target
    const data = {
      amount: parseFloat(form.amount.value),
      type: form.type.value,
      date: form.date.value,
      description: form.description.value || null,
    }

    try {
      await createTransaction(data)
      alert("Transaction saved")
      form.reset()
    } catch (error) {
      console.error(error)
      alert("Error saving transaction")
    }
  })