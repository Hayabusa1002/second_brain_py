import uuid
from typing import Optional
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password


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
        )
        return self.repository.add(user)