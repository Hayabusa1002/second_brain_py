from app.services.auth_service import AuthService


class AuthController:

    def __init__(self, service: AuthService):
        self.service = service

    def register(self, data):
        return self.service.register(data)

    def login(self, data):
        return self.service.login(data)