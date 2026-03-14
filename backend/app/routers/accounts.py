from uuid import UUID
from typing import List
from fastapi import APIRouter

from app.controllers.account_controller import AccountController
from app.services.account_service import AccountService
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountResponse

router = APIRouter()

repository = AccountRepository()
service = AccountService(repository)
controller = AccountController(service)

@router.get("/accounts", response_model=List[AccountResponse])
def list_accounts():
    return controller.list_accounts()

@router.get("/accounts/{account_id}/balance")
def get_balance(account_id: UUID):
    return controller.get_balance(account_id)