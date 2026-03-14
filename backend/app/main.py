from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routers import transactions, categories, accounts

app = FastAPI()

app.include_router(transactions.router)
app.include_router(categories.router)
app.include_router(accounts.router)

app.mount(
    "/static",
    StaticFiles(directory="../frontend/web"),
    name="static"
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def index():
    return FileResponse("../frontend/web/pages/transactions/show.html")

@app.get("/transactions/add")
def add_page():
    return FileResponse("../frontend/web/pages/transactions/add.html")

@app.get("/transactions/import")
def import_page():
    return FileResponse("../frontend/web/pages/transactions/import.html")