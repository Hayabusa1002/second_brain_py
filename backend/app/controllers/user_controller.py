from uuid import UUID

from app.schemas.user import UserCreate, UserOAuthCreate, UserUpdate
from app.services.user_service import UserService


class UserController:
    def __init__(self, service: UserService):
        self.service = service

    # ---------- Reads ----------

    def list_users(self):
        return self.service.list_users()

    def list_pending_users(self):
        return self.service.list_pending_users()

    def list_active_users(self):
        return self.service.list_active_users()

    def get_user(self, user_id: UUID):
        return self.service.get_user(user_id)

    # ---------- Writes ----------

    def create_user(self, data: UserCreate, user_id: UUID):
        return self.service.create_user(data=data, user_id=user_id)

    def create_oauth_user(self, data: UserOAuthCreate, user_id: UUID):
        return self.service.create_oauth_user(data=data, user_id=user_id)

    def update_user(self, data: UserUpdate, user_id: UUID):
        # para perfil propio
        return self.service.update_user(data=data, user_id=user_id)

    def update_user_by_admin(self, user_id: UUID, data: UserUpdate):
        # para /api/users/{user_id} (admin)
        return self.service.update_user_by_admin(target_user_id=user_id, data=data)

    def approve_user(self, user_id: UUID):
        return self.service.approve_user(user_id)

    def reject_user(self, user_id: UUID):
        return self.service.reject_user(user_id)

    def ban_user(self, user_id: UUID):
        return self.service.ban_user(user_id)

    def unban_user(self, user_id: UUID):
        return self.service.unban_user(user_id)

    def delete_user(self, user_id: UUID) -> bool:
        return self.service.delete_user(user_id)