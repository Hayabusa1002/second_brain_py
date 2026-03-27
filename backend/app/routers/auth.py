import uuid
from fastapi import APIRouter, Depends, Response, HTTPException, Cookie, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from jose import JWTError
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from app.db.deps import get_db, get_current_user
from app.controllers.auth_controller import AuthController
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin, PasswordChange, TokenResponse
from app.core.config import settings
from app.core.security import verify_password, hash_password, create_access_token, decode_token

router = APIRouter()

# OAuth client setup
_config = Config(environ={
    "GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET": settings.GOOGLE_CLIENT_SECRET,
})

oauth = OAuth(_config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
oauth.register(
    name="github",
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)


def get_controller(db: Session = Depends(get_db)) -> AuthController:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    auth_service = AuthService(user_service)
    return AuthController(auth_service)


def _set_auth_cookies(response: Response, result: TokenResponse):
    response.set_cookie(
        key="access_token", value=result.access_token,
        httponly=True, secure=settings.APP_ENV == "production",
        samesite="lax", max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token", value=result.refresh_token,
        httponly=True, secure=settings.APP_ENV == "production",
        samesite="lax", max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        path="/auth/refresh",
    )


@router.get("/auth/me")
def me(current_user=Depends(get_current_user)):
    return {"user": current_user}


@router.post("/auth/register", status_code=201)
def register(data: UserCreate, controller: AuthController = Depends(get_controller)):
    user = controller.register(data)
    return {"user": user}


@router.post("/auth/login")
def login(data: UserLogin, response: Response, controller: AuthController = Depends(get_controller)):
    result = controller.login(data)
    _set_auth_cookies(response, result)
    return {"user": result.user}


@router.post("/auth/refresh")
def refresh_token(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str | None = Cookie(default=None),
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
    try:
        from jose import jwt
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = uuid.UUID(payload["sub"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = UserRepository(db).get_by_id(user_id)
    if not user or user.status.value != "active":
        raise HTTPException(status_code=401, detail="User not found or inactive")

    new_access_token = create_access_token(user.id)
    response.set_cookie(
        key="access_token", value=new_access_token,
        httponly=True, secure=settings.APP_ENV == "production",
        samesite="lax", max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return {"message": "Token refreshed"}


@router.put("/auth/password")
def change_password(
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not verify_password(data.current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    hashed = hash_password(data.new_password)
    UserRepository(db).update_password(current_user.id, hashed)
    return {"message": "Password updated successfully"}


@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token", path="/auth/refresh")
    return {"message": "Logged out"}


# ── Google ───────────────────────────────────────────────────────────────────

@router.get("/auth/google")
async def google_login(request: Request):
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=503, detail="Google OAuth not configured")
    redirect_uri = f"{settings.APP_BASE_URL}/api/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def google_callback(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    auth_service = AuthService(UserService(UserRepository(db)))
    result = auth_service.login_or_create_oauth_user(
        email=user_info["email"],
        name=user_info.get("name", user_info["email"]),
        provider="google",
        oauth_id=user_info["sub"],
    )
    if result is None:
        return RedirectResponse("/login?status=pending", status_code=302)
    _set_auth_cookies(response, result)
    return RedirectResponse("/", status_code=302)


# ── GitHub ───────────────────────────────────────────────────────────────────

@router.get("/auth/github")
async def github_login(request: Request):
    if not settings.GITHUB_CLIENT_ID:
        raise HTTPException(status_code=503, detail="GitHub OAuth not configured")
    redirect_uri = f"{settings.APP_BASE_URL}/api/auth/github/callback"
    return await oauth.github.authorize_redirect(request, redirect_uri)

@router.get("/auth/github/callback")
async def github_callback(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    token = await oauth.github.authorize_access_token(request)
    resp = await oauth.github.get("user", token=token)
    github_user = resp.json()

    email = github_user.get("email")
    if not email:
        email_resp = await oauth.github.get("user/emails", token=token)
        emails = email_resp.json()
        primary = next((e for e in emails if e.get("primary") and e.get("verified")), None)
        email = primary["email"] if primary else None

    if not email:
        return RedirectResponse("/login?status=no_email", status_code=302)

    auth_service = AuthService(UserService(UserRepository(db)))
    result = auth_service.login_or_create_oauth_user(
        email=email,
        name=github_user.get("name") or github_user.get("login"),
        provider="github",
        oauth_id=str(github_user["id"]),
    )
    if result is None:
        return RedirectResponse("/login?status=pending", status_code=302)
    _set_auth_cookies(response, result)
    return RedirectResponse("/", status_code=302)