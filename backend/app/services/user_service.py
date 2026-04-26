from uuid import UUID

from app.core.security import hash_password
from app.models.account import AccountType
from app.models.user import UserStatus
from app.repositories.account_repository import AccountRepository
from app.repositories.user_repository import UserRepository
from app.schemas.account import AccountCreate
from app.schemas.user import UserCreate, UserOAuthCreate, UserUpdate


PERSONAL_ACCOUNT_NAME = "Personal"


class UserNotFoundError(Exception):
    def __init__(self, message: str = "User not found"):
        super().__init__(message)


class DuplicateUserEmailError(Exception):
    def __init__(self, email: str):
        super().__init__(f"User with email '{email}' already exists")


class UserService:
    def __init__(
        self,
        repository: UserRepository,
        account_repository: AccountRepository,
    ):
        self.repository = repository
        self.account_repository = account_repository

    # ---------- Reads ----------

    def list_users(self):
        return self.repository.list()

    def list_pending_users(self):
        return self.repository.list_by_status(UserStatus.pending)

    def list_active_users(self):
        return self.repository.list_by_status(UserStatus.active)

    def get_user(self, user_id: UUID):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user

    def get_user_by_email(self, email: str):
        user = self.repository.get_by_email(email)
        if not user:
            raise UserNotFoundError()
        return user

    def get_email_not_in_use(self, email: str) -> None:
        existing = self.repository.get_by_email(email)
        if existing:
            raise DuplicateUserEmailError(email)

    # ---------- Writes ----------

    def create_user(self, data: UserCreate, user_id: UUID):
        normalized_email = data.email.strip().lower()
        self.get_email_not_in_use(normalized_email)

        create_data = UserCreate(
            name=data.name.strip(),
            email=normalized_email,
            password=hash_password(data.password),
            role=data.role,
            status=data.status,
        )

        user = self.repository.create(data=create_data, user_id=user_id)
        self._create_personal_account_for_user(user.id)
        return user

    def create_oauth_user(self, data: UserOAuthCreate, user_id: UUID):
        normalized_email = data.email.strip().lower()
        self.get_email_not_in_use(normalized_email)

        oauth_data = UserOAuthCreate(
            name=data.name.strip(),
            email=normalized_email,
            provider=data.provider.strip(),
            oauth_id=data.oauth_id.strip(),
        )

        user = self.repository.create_oauth(data=oauth_data, user_id=user_id)
        self._create_personal_account_for_user(user.id)
        return user

    def update_user(self, data: UserUpdate, user_id: UUID):
        self.get_user(user_id)

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data and update_data["name"] is not None:
            update_data["name"] = update_data["name"].strip()

        if "email" in update_data and update_data["email"] is not None:
            normalized_email = update_data["email"].strip().lower()
            self.get_email_not_in_use(normalized_email)
            update_data["email"] = normalized_email

        payload = UserUpdate(**update_data)
        return self.repository.update(data=payload, user_id=user_id)


    def update_user_by_admin(self, target_user_id: UUID, data: UserUpdate):
        user = self.get_user(target_user_id)

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data and update_data["name"] is not None:
            update_data["name"] = update_data["name"].strip()

        if "email" in update_data and update_data["email"] is not None:
            normalized_email = update_data["email"].strip().lower()
            if normalized_email != user.email:
                self.get_email_not_in_use(normalized_email)
            update_data["email"] = normalized_email

        payload = UserUpdate(**update_data)

        updated = self.repository.update_by_id(
            user_id=target_user_id,
            data=payload,
        )
        if not updated:
            raise UserNotFoundError()

        return updated

    def approve_user(self, user_id: UUID):
        user = self.get_user(user_id)
        return self._change_status(user, UserStatus.active)

    def reject_user(self, user_id: UUID):
        user = self.get_user(user_id)
        return self._change_status(user, UserStatus.inactive)

    def ban_user(self, user_id: UUID):
        user = self.get_user(user_id)
        return self._change_status(user, UserStatus.banned)

    def unban_user(self, user_id: UUID):
        user = self.get_user(user_id)
        return self._change_status(user, UserStatus.active)

    def delete_user(self, user_id: UUID) -> bool:
        self.get_user(user_id)
        return self.repository.delete(user_id)

    # ---------- Helpers ----------

    def _create_personal_account_for_user(self, user_id: UUID) -> None:
        account_data = AccountCreate(
            name=PERSONAL_ACCOUNT_NAME,
            type=AccountType.individual,
        )
        account = self.account_repository.create(data=account_data, user_id=user_id)
        self.account_repository.assign_owner(account.id, user_id)

    def _change_status(self, user, new_status: UserStatus):
        updated = self.repository.update_status(user_id=user.id, status=new_status)
        if not updated:
            raise UserNotFoundError()
        return updated