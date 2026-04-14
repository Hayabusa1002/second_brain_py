from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.core.exceptions import (
    AppError,
    app_error_handler,
    generic_error_handler,
    jwt_error_handler,
    validation_error_handler,
)
from app.routers import (
    accounts,
    auth,
    categories,
    cities,
    stores,
    subcategories,
    transactions,
    users,
)
from app.routers.helpers import export


def create_app() -> FastAPI:
    app_kwargs = {}
    if settings.APP_ENV == "production":
        app_kwargs.update(
            docs_url=None,
            redoc_url=None,
            openapi_url=None,
        )

    app = FastAPI(**app_kwargs)

    register_middlewares(app)
    register_exception_handlers(app)
    register_routers(app)
    register_healthcheck(app)

    return app


def register_middlewares(app: FastAPI) -> None:
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


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(JWTError, jwt_error_handler)
    app.add_exception_handler(Exception, generic_error_handler)


def register_routers(app: FastAPI) -> None:
    api_routers = [
        auth.router,
        transactions.router,
        categories.router,
        accounts.router,
        users.router,
        export.router,
        stores.router,
        subcategories.router,
        subcategories.base_router,
        cities.router,
    ]

    for router in api_routers:
        app.include_router(router, prefix="/api")


def register_healthcheck(app: FastAPI) -> None:
    @app.get("/health")
    def health():
        return {"status": "ok"}


app = create_app()