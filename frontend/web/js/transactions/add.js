document
  .getElementById("expense-form")
  .addEventListener("submit", async (event) => {

    event.preventDefault()

    const form = event.target

    const data = {
      amount: form.amount.value,
      date: form.date.value,
      type: form.type.value
    }

    await fetch("/transactions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })

  })