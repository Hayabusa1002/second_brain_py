from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.routers import transactions, categories, accounts, auth


app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent


# API routers
app.include_router(auth.router,         prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(categories.router,   prefix="/api")
app.include_router(accounts.router,     prefix="/api")

# Static files
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "frontend/web"),
    name="static"
)

# Jinja2 templates
templates = Jinja2Templates(directory="app/templates")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("transactions/show.html", {"request": request})


@app.get("/transactions/add", response_class=HTMLResponse)
def add_page(request: Request):
    return templates.TemplateResponse("transactions/add.html", {"request": request})


@app.get("/transactions/import", response_class=HTMLResponse)
def import_page(request: Request):
    return templates.TemplateResponse("transactions/import.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})