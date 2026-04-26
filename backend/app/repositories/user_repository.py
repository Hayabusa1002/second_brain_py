from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models.user import User, UserStatus
from app.schemas.user import UserCreate, UserOAuthCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Reads ----------

    def list(self) -> List[User]:
        return (
            self.db.query(User)
            .options(selectinload(User.accounts))
            .order_by(User.name.asc())
            .all()
        )

    def list_by_status(self, status: UserStatus) -> List[User]:
        return (
            self.db.query(User)
            .options(selectinload(User.accounts))
            .filter(User.status == status)
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

    def create_oauth(self, data: UserOAuthCreate, user_id: UUID) -> User:
        user = User(
            name=data.name.strip(),
            email=data.email.strip().lower(),
            oauth_provider=data.provider.strip(),
            oauth_id=data.oauth_id.strip(),
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

    def update_by_id(self, user_id: UUID, data: UserUpdate) -> Optional[User]:
        user = self.get_by_id(user_id)
        if not user:
            return None

        allowed_fields = {"name", "email", "role", "status"}
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if field not in allowed_fields:
                continue

            if isinstance(value, str):
                value = value.strip()

            if field == "email" and value:
                value = value.lower()

            setattr(user, field, value)

        user.updated_by = user_id

        self.db.commit()
        self.db.refresh(user)
        return self.get_by_id(user.id)

    def update_status(self, user_id: UUID, status: UserStatus) -> Optional[User]:
        user = self.get_by_id(user_id)
        if not user:
            return None

        user.status = status
        user.updated_by = user_id

        self.db.commit()
        self.db.refresh(user)
        return self.get_by_id(user.id)

    def update_password(self, user_id: UUID, hashed_password: str) -> Optional[User]:
        user = self.get_by_id(user_id)
        if not user:
            return None

        user.password = hashed_password
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