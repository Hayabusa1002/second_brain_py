from fastapi import HTTPException, status
from app.services.user_service import UserService
from app.core.security import verify_password, create_access_token
from app.schemas.user import TokenResponse, UserResponse


class AuthService:

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register(self, data) -> TokenResponse:
        if self.user_service.get_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        user  = self.user_service.create_user(data)
        token = create_access_token(user.id)
        return TokenResponse(access_token=token, user=UserResponse.model_validate(user))

    def login(self, data) -> TokenResponse:
        user = self.user_service.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        token = create_access_token(user.id)
        return TokenResponse(access_token=token, user=UserResponse.model_validate(user))