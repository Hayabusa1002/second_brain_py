import uuid

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette.config import Config

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.db.deps import get_current_user, get_db
from app.schemas.user import (
    PasswordChange,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserOAuthCreate,
)
from app.controllers.auth_controller import AuthController
from app.repositories.account_repository import AccountRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService


router = APIRouter(prefix="/auth")


# ---------- OAuth client setup ----------

_config = Config(
    environ={
        "GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID,
        "GOOGLE_CLIENT_SECRET": settings.GOOGLE_CLIENT_SECRET,
    }
)

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


# ---------- Dependencies ----------

def get_controller(db: Session = Depends(get_db)) -> AuthController:
    user_repo = UserRepository(db)
    account_repo = AccountRepository(db)
    user_service = UserService(user_repo, account_repo)
    auth_service = AuthService(user_service)
    return AuthController(auth_service)


def _cookie_security_settings() -> tuple[bool, str]:
    env = (settings.APP_ENV or "development").lower()
    if env == "production":
        return True, "none"
    return False, "lax"


def _set_auth_cookies(response: Response, result: TokenResponse):
    secure, samesite = _cookie_security_settings()
    response.set_cookie(
        key="access_token",
        value=result.access_token,
        httponly=True,
        secure=secure,
        samesite=samesite,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=secure,
        samesite=samesite,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        path="/api/auth/refresh",
    )


# ---------- Me / Login / Register / Logout ----------

@router.get("/me")
def me(user=Depends(get_current_user)):
    return {"user": user}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    data: UserCreate,
    controller: AuthController = Depends(get_controller),
):
    user = controller.register(data)
    return {"user": user}


@router.post("/login")
def login(
    data: UserLogin,
    response: Response,
    controller: AuthController = Depends(get_controller),
):
    result = controller.login(data)
    _set_auth_cookies(response, result)
    return {"user": result.user}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/auth/refresh")
    return {"message": "Logged out"}


# ---------- Refresh token ----------

@router.post("/refresh")
def refresh_token(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str | None = Cookie(default=None),
):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")

    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

        user_id = uuid.UUID(payload["sub"])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    user = UserRepository(db).get_by_id(user_id)
    if not user or user.status.value != "active":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")

    new_access_token = create_access_token(user.id)
    secure, samesite = _cookie_security_settings()
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=secure,
        samesite=samesite,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    return {"message": "Token refreshed"}


# ---------- Change password ----------

@router.put("/password")
def change_password(
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not verify_password(data.current_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")

    hashed = hash_password(data.new_password)
    UserRepository(db).update_password(current_user.id, hashed)
    return {"message": "Password updated successfully"}


# ---------- Google OAuth ----------

@router.get("/google")
async def google_login(request: Request):
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Google OAuth not configured")


    redirect_uri = f"{settings.APP_BASE_URL}/api/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")


    user_service = UserService(
        UserRepository(db),
        AccountRepository(db),
    )
    auth_service = AuthService(user_service)
    controller = AuthController(auth_service)

    oauth_data = UserOAuthCreate(
        name=user_info.get("name", user_info["email"]),
        email=user_info["email"],
        provider="google",
        oauth_id=user_info["sub"],
    )

    result = controller.login_or_create_oauth_user(oauth_data)
    if result is None:
        return RedirectResponse(
            f"{settings.ALLOWED_ORIGINS[0]}/login?status=pending",
            status_code=status.HTTP_302_FOUND,
        )

    redirect = RedirectResponse(
        f"{settings.ALLOWED_ORIGINS[0]}/", 
        status_code=status.HTTP_302_FOUND
    )
    _set_auth_cookies(redirect, result)
    return redirect


# ---------- GitHub OAuth ----------

@router.get("/github")
async def github_login(request: Request):
    if not settings.GITHUB_CLIENT_ID:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="GitHub OAuth not configured")

    redirect_uri = f"{settings.APP_BASE_URL}/api/auth/github/callback"
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/github/callback")
async def github_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    token = await oauth.github.authorize_access_token(request)
    resp = await oauth.github.get("user", token=token)
    github_user = resp.json()

    email = github_user.get("email")
    if not email:
        email_resp = await oauth.github.get("user/emails", token=token)
        emails = email_resp.json()
        primary = next(
            (e for e in emails if e.get("primary") and e.get("verified")),
            None,
        )
        email = primary["email"] if primary else None

    if not email:
        return RedirectResponse(
            f"{settings.ALLOWED_ORIGINS[0]}/login?status=no_email",
            status_code=status.HTTP_302_FOUND,
        )

    user_service = UserService(
        UserRepository(db),
        AccountRepository(db),
    )
    auth_service = AuthService(user_service)
    controller = AuthController(auth_service)

    oauth_data = UserOAuthCreate(
        name=github_user.get("name") or github_user.get("login"),
        email=email,
        provider="github",
        oauth_id=str(github_user["id"]),
    )

    result = controller.login_or_create_oauth_user(oauth_data)
    if result is None:
        return RedirectResponse(
            f"{settings.ALLOWED_ORIGINS[0]}/login?status=pending",
            status_code=status.HTTP_302_FOUND,
        )

    redirect = RedirectResponse(f"{settings.ALLOWED_ORIGINS[0]}/", status_code=status.HTTP_302_FOUND)
    _set_auth_cookies(redirect, result)
    return redirect