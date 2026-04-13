from uuid import UUID

from app.schemas.user import UserCreate, UserOAuthCreate, UserUpdate
from app.services.user_service import UserService


class UserController:
    def __init__(self, service: UserService):
        self.service = service

    # ---------- Reads ----------

    def list_users(self):
        return self.service.list_users()

    def get_user(self, user_id: UUID):
        return self.service.get_user(user_id)

    # ---------- Writes ----------

    def create_user(self, data: UserCreate, user_id: UUID):
        return self.service.create_user(data=data, user_id=user_id)

    def create_oauth_user(self, data: UserOAuthCreate, user_id: UUID):
        return self.service.create_oauth_user(data=data, user_id=user_id)

    def update_user(self, data: UserUpdate, user_id: UUID):
        return self.service.update_user(data=data, user_id=user_id)

    def delete_user(self, user_id: UUID) -> bool:
        return self.service.delete_user(user_id)