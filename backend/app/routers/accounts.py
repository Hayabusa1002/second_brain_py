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
from app.models.account import AccountType


router = APIRouter()


def get_controller(db: Session = Depends(get_db)) -> AccountController:
    repository = AccountRepository(db)
    service = AccountService(repository)
    return AccountController(service, db)


def _get_account_or_404(account_id: UUID, db: Session):
    account = AccountRepository(db).get_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


def _is_owner(account, user_id: UUID) -> bool:
    return any(owner.id == user_id for owner in account.owners)


def _can_manage_account(user, account) -> bool:
    # Admin can manage any account
    if user.role == UserRole.admin:
        return True

    # Owner role can manage accounts
    if user.role == UserRole.owner:
        return True

    # Partner can only manage their own individual accounts
    if user.role == UserRole.partner:
        return account.type == AccountType.individual and _is_owner(account, user.id)

    return False


def _can_manage_shared_account_owners(user) -> bool:
    return user.role in (UserRole.admin, UserRole.owner)


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
    # Shared accounts are restricted to owner/admin roles
    if data.type == AccountType.shared and user.role not in (UserRole.admin, UserRole.owner):
        raise HTTPException(
            status_code=403,
            detail="Only owners or admins can create shared accounts",
        )

    repo = AccountRepository(db)
    account = repo.create(name=data.name, type=data.type, created_by=user.id)
    repo.assign_owner(account.id, user.id)
    db.refresh(account)
    return account


@router.put("/accounts/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: UUID,
    data: AccountUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    account = _get_account_or_404(account_id, db)

    if not _can_manage_account(user, account):
        raise HTTPException(status_code=403, detail="Not allowed")

    # Partners are allowed to manage only individual accounts
    # They must never convert an individual account into a shared one
    if user.role == UserRole.partner and data.type == AccountType.shared:
        raise HTTPException(
            status_code=403,
            detail="Partners cannot convert accounts to shared",
        )

    updated = AccountRepository(db).update(account_id, data.name, data.type)
    if not updated:
        raise HTTPException(status_code=404, detail="Account not found")
    return updated


@router.delete("/accounts/{account_id}", status_code=204)
def delete_account(
    account_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    account = _get_account_or_404(account_id, db)

    if user.role == UserRole.partner:
        if account.type == AccountType.shared:
            raise HTTPException(
                status_code=403,
                detail="Partners cannot delete shared accounts",
            )
        if not _is_owner(account, user.id):
            raise HTTPException(
                status_code=403,
                detail="You can only delete your own individual accounts",
            )

    elif user.role == UserRole.owner:
        if not _is_owner(account, user.id):
            raise HTTPException(
                status_code=403,
                detail="Owners can only delete accounts they own",
            )

    elif user.role != UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this account",
        )

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
    if not _can_manage_shared_account_owners(user):
        raise HTTPException(status_code=403, detail="Not allowed")

    repo = AccountRepository(db)
    account = repo.get_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Owners can only be assigned to shared accounts
    if account.type != AccountType.shared:
        raise HTTPException(
            status_code=400,
            detail="Owners can only be assigned to shared accounts",
        )

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
    if not _can_manage_shared_account_owners(user):
        raise HTTPException(status_code=403, detail="Not allowed")

    repo = AccountRepository(db)
    account = repo.get_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if account.type != AccountType.shared:
        raise HTTPException(
            status_code=400,
            detail="Owners can only be removed from shared accounts",
        )

    try:
        repo.unassign_owner(account_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"detail": "Owner removed"}