from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.controllers.auth_controller import AuthController
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.core.exceptions import NotFoundError


router = APIRouter()


def get_controller(db: Session = Depends(get_db)) -> AuthController:
    user_repo    = UserRepository(db)
    user_service = UserService(user_repo)
    auth_service = AuthService(user_service)
    return AuthController(auth_service)


@router.post("/auth/register", response_model=TokenResponse, status_code=201)
def register(
    data: UserCreate,
    controller: AuthController = Depends(get_controller)
):
    return controller.register(data)


@router.post("/auth/login", response_model=TokenResponse)
def login(
    data: UserLogin,
    controller: AuthController = Depends(get_controller)
):
    return controller.login(data)