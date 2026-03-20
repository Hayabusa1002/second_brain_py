from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Cookie, status, Request
from fastapi.responses import RedirectResponse
from jose import JWTError

from app.db.session import SessionLocal
from app.core.security import decode_token
from app.models.user import UserRole


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    access_token: str | None = Cookie(default=None),
):
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
    db: Session = Depends(get_db),
):
    from app.repositories.user_repository import UserRepository
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/login")
    try:
        user_id = decode_token(token)
    except Exception:
        return RedirectResponse("/login")
    user = UserRepository(db).get_by_id(user_id)
    if not user:
        return RedirectResponse("/login")
    return user


def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user