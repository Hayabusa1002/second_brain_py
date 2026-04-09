from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator

from app.models.user import UserRole, UserStatus


def validate_password_length(value: str) -> str:
    """Validate password max length for bcrypt compatibility."""
    if len(value.encode("utf-8")) > 72:
        raise ValueError("Password must be 72 characters or fewer")
    return value


class UserCreate(BaseModel):
    name:     str
    email:    EmailStr
    password: str
    role:     UserRole = UserRole.partner

    @field_validator("password")
    @classmethod
    def password_length(cls, v: str) -> str:
        return validate_password_length(v)


class UserUpdate(BaseModel):
    name:  str | None = None
    role:  UserRole | None = None


class PasswordChange(BaseModel):
    current_password: str
    new_password:     str

    @field_validator("new_password")
    @classmethod
    def password_length(cls, v: str) -> str:
        return validate_password_length(v)


class UserLogin(BaseModel):
    email:    EmailStr
    password: str


class UserResponse(BaseModel):
    id:         UUID
    name:       str
    email:      str
    role:       UserRole
    status:     UserStatus
    
    created_by: UUID
    created_at: datetime
    updated_by: UUID
    updated_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token:   str
    refresh_token:  str
    token_type:     str = "bearer"
    user:           UserResponse