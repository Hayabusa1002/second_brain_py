from fastapi import FastAPI

from app.routers import transactions, categories

app = FastAPI()

app.include_router(transactions.router)
app.include_router(categories.router)