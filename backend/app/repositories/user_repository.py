from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.user import User, UserStatus, UserRole
from app.models.account import AccountType
from app.models.transaction import Transaction


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

        try:
            # Delete every transaction created by this user first
            self.db.query(Transaction).filter(
                Transaction.created_by == user_id
            ).delete(synchronize_session=False)

            # Copy the relationship to avoid mutating the collection while iterating
            accounts = list(user.accounts)

            for account in accounts:
                # Individual accounts belong to a single user by business rule,
                # so they must be deleted when that user is deleted
                if account.type == AccountType.individual:
                    self.db.delete(account)
                    continue

                # Shared accounts are deleted only when this user is the last owner
                # Otherwise, the user is simply removed from the owners relation
                if account.type == AccountType.shared:
                    if len(account.owners) <= 1:
                        self.db.delete(account)
                    else:
                        account.owners.remove(user)

            # Delete the user only after all dependent cleanup is done
            self.db.delete(user)
            self.db.commit()
            return True

        except Exception:
            # Roll back the whole transaction so the database does not end up
            # in a partially deleted state
            self.db.rollback()
            raise

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