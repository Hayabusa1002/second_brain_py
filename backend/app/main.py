from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.db.init_db import init_db
from app.db.seed import seed
from app.db.session import SessionLocal
from app.routers import transactions, categories, accounts

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
    yield

app = FastAPI(lifespan=lifespan)

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