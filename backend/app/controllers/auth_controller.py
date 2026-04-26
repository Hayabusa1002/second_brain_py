from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserOAuthCreate, UserResponse
from app.services.auth_service import AuthService


class AuthController:
    def __init__(self, service: AuthService):
        self.service = service

    # ---------- Writes ----------

    def register(self, data: UserCreate) -> UserResponse:
        return self.service.register(data)

    def login(self, data: UserLogin) -> TokenResponse:
        return self.service.login(data)

    def login_or_create_oauth_user(self, data: UserOAuthCreate) -> TokenResponse | None:
        return self.service.login_or_create_oauth_user(data)