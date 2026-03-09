from fastapi import FastAPI

from app.routers import transactions, categories, accounts

app = FastAPI()

app.include_router(transactions.router)
app.include_router(categories.router)
app.include_router(accounts.router)