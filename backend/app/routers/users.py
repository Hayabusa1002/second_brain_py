from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db, require_admin, get_current_user
from app.models.user import User, UserStatus
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter(tags=["users"], dependencies=[Depends(require_admin)])


@router.get("/users")
def list_all_users(db: Session = Depends(get_db)):
    users = UserRepository(db).get_all()
    return {"users": [UserResponse.model_validate(u) for u in users]}


@router.get("/users/pending")
def list_pending(db: Session = Depends(get_db)):
    users = UserRepository(db).get_pending()
    return {"users": [UserResponse.model_validate(u) for u in users]}


@router.get("/users/active")
def list_active_users(db: Session = Depends(get_db)):
    users = UserRepository(db).get_active()
    return {"users": [UserResponse.model_validate(u) for u in users]}


@router.get("/users/{user_id}")
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}


@router.put("/users/{user_id}")
def update_user(user_id: UUID, data: UserUpdate, db: Session = Depends(get_db)):
    user = UserRepository(db).update(user_id, data.name, data.role)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}


@router.post("/users/{user_id}/approve")
def approve_user(user_id: UUID, db: Session = Depends(get_db)):
    user = UserRepository(db).update_status(user_id, UserStatus.active)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}


@router.post("/users/{user_id}/reject")
def reject_user(user_id: UUID, db: Session = Depends(get_db)):
    user = UserRepository(db).update_status(user_id, UserStatus.inactive)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}


@router.post("/users/{user_id}/ban")
def ban_user(user_id: UUID, db: Session = Depends(get_db)):
    user = UserRepository(db).update_status(user_id, UserStatus.banned)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}


@router.post("/users/{user_id}/unban")
def unban_user(user_id: UUID, db: Session = Depends(get_db)):
    user = UserRepository(db).update_status(user_id, UserStatus.active)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}


@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db),
):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    deleted = UserRepository(db).delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")