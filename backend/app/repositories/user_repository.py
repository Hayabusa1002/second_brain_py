from typing import Optional
from uuid import UUID
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User, UserStatus, UserRole
from app.models.account import Account


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email.lower().strip()).first()

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all(self) -> list[User]:
        return self.db.query(User).order_by(User.created_at.desc()).all()

    def get_active(self):
        return self.db.query(User).filter(User.status == UserStatus.active).all()

    def get_pending(self) -> list[User]:
        return self.db.query(User).filter(User.status == UserStatus.pending).all()

    def add(self, user: User) -> User:
        user.email = user.email.lower().strip()

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_status(self, user_id, status: UserStatus) -> User | None:
        user = self.get_by_id(user_id)
        if not user:
            return None
        user.status = status
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_password(self, user_id, hashed_password: str) -> User | None:
        user = self.get_by_id(user_id)
        if not user:
            return None
        user.password = hashed_password
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: UUID, name: str | None, role) -> User | None:
        user = self.get_by_id(user_id)
        if not user:
            return None
        if name is not None:
            user.name = name
        if role is not None:
            user.role = role
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: UUID) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False

        # Individual accounts
        sole_owned = (
            self.db.query(Account)
            .join(Account.owners)
            .filter(User.id == user_id)
            .having(func.count(User.id) == 1)
            .group_by(Account.id)
            .all()
        )
        for account in sole_owned:
            self.db.delete(account)

        # Shared accounts
        user.accounts.clear()

        self.db.delete(user)
        self.db.commit()
        return True

    def create_oauth(self, email: str, name: str, provider: str, oauth_id: str) -> User:
        user = User(
            name=name,
            email=email.lower().strip(),
            password=None,
            status=UserStatus.pending,
            role=UserRole.partner,
            oauth_provider=provider,
            oauth_id=oauth_id,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_oauth(self, user_id: UUID, provider: str, oauth_id: str) -> User | None:
        user = self.get_by_id(user_id)
        if not user:
            return None
        user.oauth_provider = provider
        user.oauth_id = oauth_id
        self.db.commit()
        self.db.refresh(user)
        return user