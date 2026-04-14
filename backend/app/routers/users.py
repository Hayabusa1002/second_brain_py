from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controllers.user_controller import UserController
from app.db.deps import get_current_user, get_db, require_admin
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserNotFoundError, UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(require_admin)],
)


def get_controller(db: Session = Depends(get_db)) -> UserController:
    user_repository = UserRepository(db)
    account_repository = AccountRepository(db)
    service = UserService(
        repository=user_repository,
        account_repository=account_repository,
    )
    return UserController(service)


# ---------- Reads ----------

@router.get("", response_model=List[UserResponse])
def list_all_users(
    controller: UserController = Depends(get_controller),
):
    return controller.list_users()


@router.get("/pending", response_model=List[UserResponse])
def list_pending_users(
    controller: UserController = Depends(get_controller),
):
    return controller.list_pending_users()


@router.get("/active", response_model=List[UserResponse])
def list_active_users(
    controller: UserController = Depends(get_controller),
):
    return controller.list_active_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    controller: UserController = Depends(get_controller),
):
    try:
        return controller.get_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


# ---------- Writes ----------

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    data: UserUpdate,
    controller: UserController = Depends(get_controller),
):
    try:
        return controller.update_user_by_admin(user_id=user_id, data=data)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{user_id}/approve", response_model=UserResponse)
def approve_user(
    user_id: UUID,
    controller: UserController = Depends(get_controller),
):
    try:
        return controller.approve_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{user_id}/reject", response_model=UserResponse)
def reject_user(
    user_id: UUID,
    controller: UserController = Depends(get_controller),
):
    try:
        return controller.reject_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{user_id}/ban", response_model=UserResponse)
def ban_user(
    user_id: UUID,
    controller: UserController = Depends(get_controller),
):
    try:
        return controller.ban_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{user_id}/unban", response_model=UserResponse)
def unban_user(
    user_id: UUID,
    controller: UserController = Depends(get_controller),
):
    try:
        return controller.unban_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    user: User = Depends(get_current_user),
    controller: UserController = Depends(get_controller),
):
    if user_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account",
        )

    try:
        return controller.delete_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))