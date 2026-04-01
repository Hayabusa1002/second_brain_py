from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db, require_admin, get_current_user
from app.models.user import User, UserStatus
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter(tags=["users"], dependencies=[Depends(require_admin)])


def _get_user_or_404(user_id: UUID, db: Session) -> User:
    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


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
    user = _get_user_or_404(user_id, db)
    return {"user": UserResponse.model_validate(user)}


@router.put("/users/{user_id}")
def update_user(user_id: UUID, data: UserUpdate, db: Session = Depends(get_db)):
    user = UserRepository(db).update(user_id, data.name, data.role)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": UserResponse.model_validate(user)}


@router.post("/users/{user_id}/approve")
def approve_user(user_id: UUID, db: Session = Depends(get_db)):
    user = _get_user_or_404(user_id, db)

    if user.status != UserStatus.pending:
        raise HTTPException(
            status_code=400,
            detail="Only pending users can be approved"
        )

    user = UserRepository(db).update_status(user_id, UserStatus.active)
    return {"user": UserResponse.model_validate(user)}


@router.post("/users/{user_id}/reject")
def reject_user(user_id: UUID, db: Session = Depends(get_db)):
    user = _get_user_or_404(user_id, db)

    if user.status != UserStatus.pending:
        raise HTTPException(
            status_code=400,
            detail="Only pending users can be rejected"
        )

    user = UserRepository(db).update_status(user_id, UserStatus.inactive)
    return {"user": UserResponse.model_validate(user)}


@router.post("/users/{user_id}/ban")
def ban_user(user_id: UUID, db: Session = Depends(get_db)):
    user = _get_user_or_404(user_id, db)

    if user.status != UserStatus.active:
        raise HTTPException(
            status_code=400,
            detail="Only active users can be banned"
        )

    user = UserRepository(db).update_status(user_id, UserStatus.banned)
    return {"user": UserResponse.model_validate(user)}


@router.post("/users/{user_id}/unban")
def unban_user(user_id: UUID, db: Session = Depends(get_db)):
    user = _get_user_or_404(user_id, db)

    if user.status != UserStatus.banned:
        raise HTTPException(
            status_code=400,
            detail="Only banned users can be unbanned"
        )

    user = UserRepository(db).update_status(user_id, UserStatus.active)
    return {"user": UserResponse.model_validate(user)}


@router.post("/users/{user_id}/reopen")
def reopen_user_request(user_id: UUID, db: Session = Depends(get_db)):
    user = _get_user_or_404(user_id, db)

    if user.status != UserStatus.inactive:
        raise HTTPException(
            status_code=400,
            detail="Only inactive users can reopen their request"
        )

    user = UserRepository(db).update_status(user_id, UserStatus.pending)
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