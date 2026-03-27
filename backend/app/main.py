from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
from jose import JWTError

from app.routers import transactions, categories, accounts, users, auth
from app.db.deps import get_current_user_from_cookie
from app.models.user import UserRole
from app.core.config import settings
from app.core.exceptions import (
    AppError,
    UnauthenticatedRedirect,
    app_error_handler,
    validation_error_handler,
    jwt_error_handler,
    generic_error_handler,
    unauthenticated_redirect_handler,
)

app = FastAPI()

# Required by Authlib to store OAuth state between redirect and callback
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

BASE_DIR = Path(__file__).resolve().parent.parent

# Exception handlers
app.add_exception_handler(UnauthenticatedRedirect, unauthenticated_redirect_handler)
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(JWTError, jwt_error_handler)
app.add_exception_handler(Exception, generic_error_handler)

# API routers
app.include_router(auth.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(accounts.router, prefix="/api")
app.include_router(users.router, prefix="/api")


# Service-Worker-Allowed: before load the StaticFiles from mount()
@app.get("/static/sw.js")
async def service_worker():
    sw_path = BASE_DIR.parent / "frontend/web/sw.js"
    return FileResponse(
        sw_path,
        media_type="application/javascript",
        headers={"Service-Worker-Allowed": "/"},
    )


# Static files
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR.parent / "frontend/web"),
    name="static"
)


# Jinja2 templates
templates = Jinja2Templates(directory=BASE_DIR / "app/templates")


# Routes
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@app.get("/access-requests", response_class=HTMLResponse)
def admin_access_requests(request: Request, user=Depends(get_current_user_from_cookie)):
    if user.role != UserRole.admin:
        return RedirectResponse("/")
    return templates.TemplateResponse("auth/access_requests.html", {
        "request": request,
        "user": user
    })


@app.get("/change-password", response_class=HTMLResponse)
def change_password_page(request: Request, user=Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("auth/change_password.html", {
        "request": request,
        "user": user
    })


@app.get("/", response_class=HTMLResponse)
def index(request: Request, user=Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("transactions/main.html", {
        "request": request,
        "user": user
    })


@app.get("/accounts", response_class=HTMLResponse)
def accounts_page(request: Request, user=Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("accounts/main.html", {
        "request": request,
        "user": user
    })


@app.get("/users", response_class=HTMLResponse)
def users_page(request: Request, user=Depends(get_current_user_from_cookie)):
    if user.role != UserRole.admin:
        return RedirectResponse("/")
    return templates.TemplateResponse("users/main.html", {
        "request": request,
        "user": user,
    })