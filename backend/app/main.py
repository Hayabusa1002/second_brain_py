from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from jose import JWTError

from app.routers import (
    transactions,
    categories,
    accounts,
    users,
    auth,
    export,
    stores,
    subcategories,
    cities,
)
from app.core.config import settings
from app.core.exceptions import (
    AppError,
    app_error_handler,
    validation_error_handler,
    jwt_error_handler,
    generic_error_handler,
)

if settings.APP_ENV == "production":
    app = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
else:
    app = FastAPI()


# Required by Authlib to store OAuth state between redirect and callback
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
)


# Exception handlers
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
app.include_router(export.router, prefix="/api")
app.include_router(stores.router, prefix="/api")
app.include_router(subcategories.router, prefix="/api")
app.include_router(cities.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}