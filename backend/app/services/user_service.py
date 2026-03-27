from uuid import UUID
from app.repositories.user_repository import UserRepository
from app.models.user import User, UserStatus, UserRole
from app.core.security import hash_password
from app.core.exceptions import NotFoundError

PERSONAL_ACCOUNT_NAME = "Personal"


class UserService:
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_by_email(self, email: str) -> User | None:
        return self.user_repo.get_by_email(email)

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.user_repo.get_by_id(user_id)

    def create_user(self, name: str, email: str, password: str, role: UserRole = UserRole.partner) -> User:
        hashed = hash_password(password)
        user = User(
            name=name,
            email=email,
            password=hashed,
            role=role,
            status=UserStatus.pending,
        )
        return self.user_repo.add(user)
    
    def delete_user(self, user_id: UUID) -> bool:
        return self.repository.delete(user_id)

    def create_oauth_user(self, email: str, name: str, provider: str, oauth_id: str) -> User:
        return self.user_repo.create_oauth(
            email=email,
            name=name,
            provider=provider,
            oauth_id=oauth_id,
        )

    def update_oauth(self, user_id: UUID, provider: str, oauth_id: str) -> User | None:
        return self.user_repo.update_oauth(user_id, provider, oauth_id)