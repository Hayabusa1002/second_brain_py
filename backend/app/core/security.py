import uuid
from datetime import datetime, timedelta, UTC
import bcrypt
from jose import jwt

from app.core.config import settings

# Sign algorithm that JWT use to generate and verify tokens
ALGORITHM = "HS256"


def _safe(password: str) -> str:
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")


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