import uuid
from typing import Optional

from app.models.user import User, UserStatus, UserRole
from app.models.account import Account, AccountType
from app.models.account_owner import account_owners
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password


PERSONAL_ACCOUNT_NAME = "Personal"

class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_by_email(self, email: str) -> Optional[User]:
        return self.repository.get_by_email(email)

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return self.repository.get_by_id(user_id)

    def create_user(self, data) -> User:
        user = User(
            id=uuid.uuid4(),
            name=data.name,
            email=data.email,
            password=hash_password(data.password),
            status=UserStatus.pending,
            role=UserRole.partner,
        )
        db = self.repository.db
        db.add(user)
        db.flush()

        personal_account = Account(
            id=uuid.uuid4(),
            name=PERSONAL_ACCOUNT_NAME,
            type=AccountType.individual,
            created_by=user.id,
        )
        db.add(personal_account)
        db.flush()

        db.execute(
            account_owners.insert().values(
                account_id=personal_account.id,
                user_id=user.id,
            )
        )

        db.commit()
        db.refresh(user)
        return user