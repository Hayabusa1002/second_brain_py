from uuid import UUID
from app.repositories.user_repository import UserRepository
from app.repositories.account_repository import AccountRepository
from app.models.user import User, UserStatus, UserRole
from app.models.account import AccountType
from app.core.security import hash_password

PERSONAL_ACCOUNT_NAME = "Personal"


class UserService:
    
    def __init__(self, user_repo: UserRepository, account_repo: AccountRepository):
        self.user_repo = user_repo
        self.account_repo = account_repo

    def get_by_email(self, email: str) -> User | None:
        return self.user_repo.get_by_email(email)

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.user_repo.get_by_id(user_id)

    def create_user(
        self,
        name: str,
        email: str,
        password: str,
        role: UserRole = UserRole.partner
    ) -> User:
        hashed = hash_password(password)
        user = User(
            name=name,
            email=email,
            password=hashed,
            role=role,
            status=UserStatus.pending,
        )
        user = self.user_repo.add(user)
        self._create_personal_account_for_user(user.id)
        return user
    
    def delete_user(self, user_id: UUID) -> bool:
        return self.user_repo.delete(user_id)

    def create_oauth_user(self, email: str, name: str, provider: str, oauth_id: str) -> User:
        user = self.user_repo.create_oauth(
            email=email,
            name=name,
            provider=provider,
            oauth_id=oauth_id,
        )
        self._create_personal_account_for_user(user.id)
        return user

    def update_oauth(self, user_id: UUID, provider: str, oauth_id: str) -> User | None:
        return self.user_repo.update_oauth(user_id, provider, oauth_id)

    def _create_personal_account_for_user(self, user_id: UUID) -> None:
        account = self.account_repo.create(
            name=PERSONAL_ACCOUNT_NAME,
            type=AccountType.individual,
            created_by=user_id,
        )
        self.account_repo.assign_owner(account.id, user_id)