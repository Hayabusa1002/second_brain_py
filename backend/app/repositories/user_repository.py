from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.user import User, UserStatus

class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def add(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_pending(self) -> list[User]:
        return self.db.query(User).filter(User.status == UserStatus.pending).all()

    def update_status(self, user_id, status: UserStatus) -> User | None:
        user = self.get_by_id(user_id)
        if not user:
            return None
        user.status = status
        self.db.commit()
        self.db.refresh(user)
        return user