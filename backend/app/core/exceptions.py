from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from jose import JWTError


class AppError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


# 404
class NotFoundError(AppError):
    def __init__(self, resource: str):
        super().__init__(404, f"{resource} not found")


# 403
class ForbiddenError(AppError):
    def __init__(self):
        super().__init__(403, "Access forbidden")


# 401 → redirect to login (HTML/Jinja2 routes only)
class UnauthenticatedRedirect(Exception):
    pass


# Handlers
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = [{"field": e["loc"][-1], "message": e["msg"]} for e in exc.errors()]
    return JSONResponse(status_code=422, content={"detail": errors})

async def jwt_error_handler(request: Request, exc: JWTError):
    return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

async def generic_error_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

async def unauthenticated_redirect_handler(request: Request, exc: UnauthenticatedRedirect):
    """ Redirects to login when session is expired or missing on HTML routes """
    return RedirectResponse("/login", status_code=302)