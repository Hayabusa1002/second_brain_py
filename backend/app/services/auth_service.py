from fastapi import HTTPException
from app.services.user_service import UserService
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.schemas.user import TokenResponse, UserResponse
from app.models.user import UserStatus


class AuthService:

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register(self, data) -> UserResponse:
        if self.user_service.get_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        user = self.user_service.create_user(
            name=data.name,
            email=data.email,
            password=data.password,
        )
        return UserResponse.model_validate(user)

    def login(self, data) -> TokenResponse:
        user = self.user_service.get_by_email(data.email)
        if not user or not user.password or not verify_password(data.password, user.password):
            # OAuth users have no password — block cleanly before bcrypt crash
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if user.status == UserStatus.pending:
            raise HTTPException(status_code=403, detail="Pending request")
        if user.status != UserStatus.active:
            raise HTTPException(status_code=403, detail="Account disabled")
        return self._build_token_response(user)

    def login_or_create_oauth_user(
        self, email: str, name: str, provider: str, oauth_id: str
    ) -> TokenResponse | None:
        """
        Links OAuth to existing account or creates a new pending user.
        Returns TokenResponse if active, None if pending approval.
        """
        user = self.user_service.get_by_email(email)

        if user:
            # Link OAuth provider to existing account if not already linked
            if not user.oauth_provider:
                self.user_service.update_oauth(user.id, provider, oauth_id)
            if user.status == UserStatus.pending:
                return None
            if user.status != UserStatus.active:
                raise HTTPException(status_code=403, detail="Account disabled")
        else:
            # New user, pending until admin approves
            self.user_service.create_oauth_user(
                email=email,
                name=name,
                provider=provider,
                oauth_id=oauth_id,
            )
            return None

        return self._build_token_response(user)

    def _build_token_response(self, user) -> TokenResponse:
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
            user=UserResponse.model_validate(user)
        )