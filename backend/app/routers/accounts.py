from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.controllers.account_controller import AccountController
from app.services.account_service import AccountService
from app.repositories.account_repository import AccountRepository
from app.repositories.user_repository import UserRepository
from app.schemas.account import AccountResponse, AccountCreate, AccountUpdate
from app.schemas.user import UserResponse
from app.core.exceptions import NotFoundError
from app.models.user import UserRole

router = APIRouter()


def get_controller(db: Session = Depends(get_db)) -> AccountController:
    repository = AccountRepository(db)
    service    = AccountService(repository)
    return AccountController(service, db)


@router.get("/accounts", response_model=List[AccountResponse])
def list_accounts(
    controller: AccountController = Depends(get_controller),
    user=Depends(get_current_user)
):
    return controller.list_accounts(user_id=user.id)


@router.get("/accounts/{account_id}/balance")
def get_balance(
    account_id: UUID,
    controller: AccountController = Depends(get_controller),
    user=Depends(get_current_user)
):
    balance = controller.get_balance(account_id)
    if balance is None:
        raise NotFoundError("Account")
    return balance


@router.get("/accounts/users/active")
def list_active_users(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role not in (UserRole.admin, UserRole.owner):
        raise HTTPException(status_code=403, detail="Not allowed")
    users = UserRepository(db).get_active()
    return {"users": [UserResponse.model_validate(u) for u in users]}


@router.post("/accounts", response_model=AccountResponse, status_code=201)
def create_account(
    data: AccountCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role not in (UserRole.admin, UserRole.owner):
        raise HTTPException(status_code=403, detail="Not allowed")
    repo = AccountRepository(db)
    account = repo.create(name=data.name, type=data.type, created_by=user.id)
    repo.assign_owner(account.id, user.id)
    return account


@router.put("/accounts/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: UUID,
    data: AccountUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role not in (UserRole.admin, UserRole.owner):
        raise HTTPException(status_code=403, detail="Not allowed")
    account = AccountRepository(db).update(account_id, data.name, data.type)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.delete("/accounts/{account_id}", status_code=204)
def delete_account(
    account_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role not in (UserRole.admin, UserRole.owner):
        raise HTTPException(status_code=403, detail="Not allowed")
    deleted = AccountRepository(db).delete(account_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Account not found")


@router.post("/accounts/{account_id}/owners/{user_id}", status_code=200)
def assign_owner(
    account_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role not in (UserRole.admin, UserRole.owner):
        raise HTTPException(status_code=403, detail="Not allowed")
    repo = AccountRepository(db)
    if not repo.get_by_id(account_id):
        raise HTTPException(status_code=404, detail="Account not found")
    try:
        repo.assign_owner(account_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "Owner assigned"}


@router.delete("/accounts/{account_id}/owners/{user_id}", status_code=200)
def unassign_owner(
    account_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role not in (UserRole.admin, UserRole.owner):
        raise HTTPException(status_code=403, detail="Not allowed")
    repo = AccountRepository(db)
    if not repo.get_by_id(account_id):
        raise HTTPException(status_code=404, detail="Account not found")
    try:
        repo.unassign_owner(account_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "Owner removed"}