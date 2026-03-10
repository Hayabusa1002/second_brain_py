import { createTransaction } from "../api/transactions.js"

document
  .getElementById("transaction-form")
  .addEventListener("submit", async (event) => {

    event.preventDefault()

    const form = event.target
    const data = {
      amount: form.amount.value,
      type: form.type.value,
      date: form.date.value
    }

    try {
      await createTransaction(data)
      alert("Transaction created")
      form.reset()
    } catch (error) {
      console.error(error)
      alert("Error creating transaction")
    }
  })