from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db, require_admin
from app.models.user import UserStatus
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.get("/users/pending")
def list_pending(
    db: Session = Depends(get_db),
    _=Depends(require_admin)
):
    users = UserRepository(db).get_pending()
    return {"users": [UserResponse.model_validate(u) for u in users]}


@router.get("/users/active")
def list_active_users(
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    users = UserRepository(db).get_active()
    return {"users": [UserResponse.model_validate(u) for u in users]}


@router.post("/users/{user_id}/approve")
def approve_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    user = UserRepository(db).update_status(user_id, UserStatus.active)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}


@router.post("/users/{user_id}/reject")
def reject_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    user = UserRepository(db).update_status(user_id, UserStatus.inactive)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}