from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pathlib import Path

from app.routers import transactions, categories, accounts, auth, admin
from app.core.security import get_current_user_from_cookie
from app.db.deps import get_current_user
from app.models.user import UserRole

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent


# API routers
app.include_router(auth.router,         prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(categories.router,   prefix="/api")
app.include_router(accounts.router,     prefix="/api")
app.include_router(admin.router,        prefix="/api")

# Static files
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR.parent / "frontend/web"),
    name="static"
)

# Jinja2 templates
templates = Jinja2Templates(directory=BASE_DIR / "app/templates")


# Endpoints
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@app.get("/change-password", response_class=HTMLResponse)
def change_password_page(request: Request, user=Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("auth/change_password.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
def index(request: Request, user=Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("transactions/show.html", {"request": request})


@app.get("/transactions/add", response_class=HTMLResponse)
def add_page(request: Request, user=Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("transactions/add.html", {"request": request})


@app.get("/transactions/import", response_class=HTMLResponse)
def import_page(request: Request, user=Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("transactions/import.html", {"request": request})


@app.get("/admin/access-requests", response_class=HTMLResponse)
def admin_access_requests(request: Request, current_user=Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        return RedirectResponse("/")
    return templates.TemplateResponse("admin/access_requests.html", {"request": request})