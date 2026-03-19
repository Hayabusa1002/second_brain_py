from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.controllers.auth_controller import AuthController
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.config import settings

router = APIRouter()


def get_controller(db: Session = Depends(get_db)) -> AuthController:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    auth_service = AuthService(user_service)
    return AuthController(auth_service)


@router.get("/auth/me")
def me(current_user = Depends(get_current_user)):
    return {"user": current_user}


@router.post("/auth/register", status_code=201)
def register(
    data: UserCreate,
    controller: AuthController = Depends(get_controller)
):
    user = controller.register(data)
    return {"user": user}


@router.post("/auth/login")
def login(
    data: UserLogin,
    response: Response,
    controller: AuthController = Depends(get_controller)
):
    result = controller.login(data)
    response.set_cookie(
        key="access_token",
        value=result.access_token,
        httponly=True,
        secure=settings.APP_ENV == "production",
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_DAYS * 86400,
    )
    return {"user": result.user}


@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}