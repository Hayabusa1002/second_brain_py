import uuid
from fastapi import APIRouter, Depends, Response, HTTPException, Cookie
from sqlalchemy.orm import Session
from jose import JWTError
from app.db.deps import get_db, get_current_user
from app.controllers.auth_controller import AuthController
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin, PasswordChange
from app.core.config import settings
from app.core.security import verify_password, hash_password, create_access_token, decode_token

router = APIRouter()


def get_controller(db: Session = Depends(get_db)) -> AuthController:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    auth_service = AuthService(user_service)
    return AuthController(auth_service)


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
    # Access token: corto (minutos)
    response.set_cookie(
        key="access_token",
        value=result.access_token,
        httponly=True,
        secure=settings.APP_ENV == "production",
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    # Refresh token: largo (días)
    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=settings.APP_ENV == "production",
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        path="/auth/refresh",
    )
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
        payload = __import__('jose').jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=["HS256"]
        )
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
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=settings.APP_ENV == "production",
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
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