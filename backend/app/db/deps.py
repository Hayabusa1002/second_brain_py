import uuid
from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Cookie, status, Request, Response
from jose import JWTError, ExpiredSignatureError

from app.db.session import SessionLocal
from app.core.security import decode_token, create_access_token
from app.core.config import settings
from app.core.exceptions import UnauthenticatedRedirect
from app.models.user import UserRole


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _try_silent_refresh(refresh_token_val: str, response: Response) -> str | None:
    """Validates the refresh token and issues a new access token cookie. Returns new token or None."""
    try:
        from jose import jwt
        payload = jwt.decode(refresh_token_val, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            return None
        user_id = uuid.UUID(payload["sub"])
        new_token = create_access_token(user_id)
        response.set_cookie(
            key="access_token",
            value=new_token,
            httponly=True,
            secure=settings.APP_ENV == "production",
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return new_token
    except Exception:
        return None


def get_current_user(
    db: Session = Depends(get_db),
    access_token: str | None = Cookie(default=None),
):
    """API routes only. Raises 401 — JS interceptor handles the refresh cycle."""
    from app.repositories.user_repository import UserRepository
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        user_id = decode_token(access_token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def get_current_user_from_cookie(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    """HTML routes only. Silently refreshes the access token if expired, or redirects to login."""
    from app.repositories.user_repository import UserRepository

    token = request.cookies.get("access_token")
    refresh = request.cookies.get("refresh_token")

    if token:
        try:
            decode_token(token)
        except ExpiredSignatureError:
            token = _try_silent_refresh(refresh, response) if refresh else None
            if not token:
                raise UnauthenticatedRedirect()
        except JWTError:
            raise UnauthenticatedRedirect()
    else:
        token = _try_silent_refresh(refresh, response) if refresh else None
        if not token:
            raise UnauthenticatedRedirect()

    try:
        user_id = decode_token(token)
    except Exception:
        raise UnauthenticatedRedirect()

    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise UnauthenticatedRedirect()
    return user


def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user