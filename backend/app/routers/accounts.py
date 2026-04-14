from typing import List
from uuid import UUID


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app.controllers.account_controller import AccountController
from app.db.deps import get_current_user, get_db
from app.models.user import UserRole
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountCreate, AccountResponse, AccountUpdate
from app.services.account_service import (
    AccountNotFoundError,
    AccountService,
    DuplicateAccountNameError,
    IndividualAccountOwnerLimitError,
    IndividualAccountOwnerModificationError,
)
from app.services.helpers.balance_service import BalanceService



router = APIRouter(prefix="/accounts")



def require_account_management_role(user=Depends(get_current_user)):
    if user.role not in (UserRole.admin, UserRole.owner):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    return user



def get_controller(db: Session = Depends(get_db)) -> AccountController:
    repository = AccountRepository(db)
    service = AccountService(repository)
    balance_service = BalanceService()
    return AccountController(service=service, balance_service=balance_service)



# ---------- Reads ----------

@router.get("/", response_model=List[AccountResponse])
def list_accounts(
    controller: AccountController = Depends(get_controller),
    user=Depends(get_current_user),
):
    return controller.list_accounts(user_id=user.id)



@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: UUID,
    controller: AccountController = Depends(get_controller),
):
    try:
        return controller.get_account(account_id)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))



@router.get("/{account_id}/balance")
def get_balance(
    account_id: UUID,
    controller: AccountController = Depends(get_controller),
):
    try:
        return controller.get_balance(account_id)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))



# ---------- Writes ----------

@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    data: AccountCreate,
    controller: AccountController = Depends(get_controller),
    user=Depends(require_account_management_role),
):
    try:
        account = controller.create_account(data=data, user_id=user.id)
        controller.assign_owner(account_id=account.id, user_id=user.id)
        return account
    except DuplicateAccountNameError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



@router.put("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: UUID,
    data: AccountUpdate,
    controller: AccountController = Depends(get_controller),
    user=Depends(require_account_management_role),
):
    try:
        return controller.update_account(
            account_id=account_id,
            data=data,
            user_id=user.id,
        )
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateAccountNameError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: UUID,
    controller: AccountController = Depends(get_controller),
):
    try:
        controller.delete_account(account_id)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))



# ---------- Owners assignation ----------

@router.post("/{account_id}/owners/{user_id}", status_code=status.HTTP_200_OK)
def assign_owner(
    account_id: UUID,
    controller: AccountController = Depends(get_controller),
    user=Depends(require_account_management_role),
):
    try:
        controller.assign_owner(account_id=account_id, user_id=user.id)
        return {"detail": "Owner assigned"}
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except IndividualAccountOwnerLimitError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



@router.delete("/{account_id}/owners/{user_id}", status_code=status.HTTP_200_OK)
def unassign_owner(
    account_id: UUID,
    controller: AccountController = Depends(get_controller),
    user=Depends(require_account_management_role),
):
    try:
        controller.unassign_owner(account_id=account_id, user_id=user.id)
        return {"detail": "Owner removed"}
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except IndividualAccountOwnerModificationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))