import uuid
from datetime import datetime, timedelta, UTC
import bcrypt
from jose import jwt
from fastapi import Request, HTTPException
from app.core.config import settings

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    pw = password.encode("utf-8")[:72]
    return bcrypt.hashpw(pw, bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    pw = plain.encode("utf-8")[:72]
    return bcrypt.checkpw(pw, hashed.encode())


def create_access_token(user_id: uuid.UUID) -> str:
    expire  = datetime.now(UTC) + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> uuid.UUID:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    return uuid.UUID(payload["sub"])


def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=307, headers={"Location": "/login"})
    try:
        return decode_token(token)
    except Exception:
        raise HTTPException(status_code=307, headers={"Location": "/login"})