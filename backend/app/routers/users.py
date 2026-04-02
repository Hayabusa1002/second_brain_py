from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db, require_admin, get_current_user
from app.models.user import User, UserStatus
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse, UserUpdate


router = APIRouter(tags=["users"], dependencies=[Depends(require_admin)])


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


@router.get("/users")
def list_all_users(repo: UserRepository = Depends(get_user_repo)):
    users = repo.get_all()
    return {"users": [UserResponse.model_validate(u) for u in users]}


@router.get("/users/pending")
def list_pending(repo: UserRepository = Depends(get_user_repo)):
    users = repo.get_pending()
    return {"users": [UserResponse.model_validate(u) for u in users]}


@router.get("/users/active")
def list_active_users(repo: UserRepository = Depends(get_user_repo)):
    users = repo.get_active()
    return {"users": [UserResponse.model_validate(u) for u in users]}


@router.get("/users/{user_id}")
def get_user(user_id: UUID, repo: UserRepository = Depends(get_user_repo)):
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}


@router.put("/users/{user_id}")
def update_user(
    user_id: UUID,
    data: UserUpdate,
    repo: UserRepository = Depends(get_user_repo),
):
    user = repo.update(user_id, data.name, data.role)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}


@router.post("/users/{user_id}/approve")
def approve_user(user_id: UUID, repo: UserRepository = Depends(get_user_repo)):
    user = repo.update_status(user_id, UserStatus.active)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}


@router.post("/users/{user_id}/reject")
def reject_user(user_id: UUID, repo: UserRepository = Depends(get_user_repo)):
    user = repo.update_status(user_id, UserStatus.inactive)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}


@router.post("/users/{user_id}/ban")
def ban_user(user_id: UUID, repo: UserRepository = Depends(get_user_repo)):
    user = repo.update_status(user_id, UserStatus.banned)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}


@router.post("/users/{user_id}/unban")
def unban_user(user_id: UUID, repo: UserRepository = Depends(get_user_repo)):
    user = repo.update_status(user_id, UserStatus.active)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}


@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    repo: UserRepository = Depends(get_user_repo),
):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")

    deleted = repo.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None