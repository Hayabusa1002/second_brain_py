from fastapi import HTTPException, status

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
        user = self.user_service.create_user(data)
        return UserResponse.model_validate(user)

    def login(self, data) -> TokenResponse:
        user = self.user_service.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if user.status == UserStatus.pending:
            raise HTTPException(status_code=403, detail="Pending request")
        if user.status != UserStatus.active:
            raise HTTPException(status_code=403, detail="Account disabled")
        
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.model_validate(user)
        )