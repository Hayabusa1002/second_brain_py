from fastapi import HTTPException

from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.models.user import UserStatus
from app.schemas.user import TokenResponse, UserLogin, UserResponse, UserCreate, UserOAuthCreate
from app.services.user_service import (
    UserService,
    DuplicateUserEmailError,
    UserNotFoundError,
)


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    # ---------- Writes ----------

    def register(self, data: UserCreate) -> UserResponse:
        try:
            user = self.user_service.create_user(data=data, user_id=None)
        except DuplicateUserEmailError:
            raise HTTPException(status_code=400, detail="Email already registered")
        except Exception:
            raise HTTPException(status_code=500, detail="Unable to register user")
        return UserResponse.model_validate(user)

    def login(self, data: UserLogin) -> TokenResponse:
        try:
            user = self.user_service.get_by_email(data.email)
        except UserNotFoundError:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not user.password or not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if user.status == UserStatus.pending:
            raise HTTPException(status_code=403, detail="Pending request")

        if user.status != UserStatus.active:
            raise HTTPException(status_code=403, detail="Account disabled")

        return self._build_token_response(user)
    
    def login_or_create_oauth_user(self, data: UserOAuthCreate) -> TokenResponse | None:
        """
        Links OAuth to existing account or creates a new pending user.
        Returns TokenResponse if active, None if pending approval.
        """
        try:
            user = self.user_service.get_by_email(data.email)
        except UserNotFoundError:
            self.user_service.create_oauth_user(data=data, user_id=None)
            return None

        if not getattr(user, "oauth_provider", None):
            self.user_service.update_oauth(
                user_id=user.id,
                provider=data.provider,
                oauth_id=data.oauth_id,
            )

        if user.status == UserStatus.pending:
            return None

        if user.status != UserStatus.active:
            raise HTTPException(status_code=403, detail="Account disabled")

        return self._build_token_response(user)

    # ---------- Helpers ----------

    def _build_token_response(self, user) -> TokenResponse:
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
            user=UserResponse.model_validate(user),
        )