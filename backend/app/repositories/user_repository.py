from typing import Optional
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session, selectinload

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Reads ----------

    def list(self) -> list[User]:
        return (
            self.db.query(User)
            .options(selectinload(User.accounts))
            .order_by(User.name.asc())
            .all()
        )

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return (
            self.db.query(User)
            .options(selectinload(User.accounts))
            .filter(User.id == user_id)
            .first()
        )

    def get_by_email(self, email: str) -> Optional[User]:
        return (
            self.db.query(User)
            .options(selectinload(User.accounts))
            .filter(User.email.ilike(email.strip()))
            .first()
        )

    def get_by_name(self, name: str) -> Optional[User]:
        return (
            self.db.query(User)
            .options(selectinload(User.accounts))
            .filter(User.name.ilike(name.strip()))
            .first()
        )

    def get_by_email_or_name(self, value: str) -> Optional[User]:
        value = value.strip()
        return (
            self.db.query(User)
            .options(selectinload(User.accounts))
            .filter(
                or_(
                    User.email.ilike(value),
                    User.name.ilike(value),
                )
            )
            .first()
        )

    # ---------- Writes ----------

    def create(self, data: UserCreate, user_id: UUID) -> User:
        user = User(
            name=data.name.strip(),
            email=data.email.strip().lower(),
            password=data.password,
            role=data.role,
            status=data.status,
            created_by=user_id,
            updated_by=user_id,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return self.get_by_id(user.id)

    def update(self, data: UserUpdate, user_id: UUID) -> Optional[User]:
        user = self.get_by_id(user_id)
        if not user:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            if isinstance(value, str):
                value = value.strip()

            if field == "email" and value:
                value = value.lower()

            setattr(user, field, value)

        user.updated_by = user_id

        self.db.commit()
        self.db.refresh(user)
        return self.get_by_id(user.id)

    def delete(self, user_id: UUID) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False

        self.db.delete(user)
        self.db.commit()
        return True