from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.controllers.account_controller import AccountController
from app.services.account_service import AccountService
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountResponse
from app.core.exceptions import NotFoundError

router = APIRouter()


def get_controller(db: Session = Depends(get_db)) -> AccountController:
    repository = AccountRepository(db)
    service    = AccountService(repository)
    return AccountController(service, db)


@router.get("/accounts", response_model=List[AccountResponse])
def list_accounts(
    controller: AccountController = Depends(get_controller),
    current_user=Depends(get_current_user)
):
    return controller.list_accounts(user_id=current_user.id)


@router.get("/accounts/{account_id}/balance")
def get_balance(
    account_id: UUID,
    controller: AccountController = Depends(get_controller),
    current_user=Depends(get_current_user)
):
    return controller.get_balance(account_id)

raise NotFoundError("Account")