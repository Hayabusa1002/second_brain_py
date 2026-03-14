from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Query

from app.controllers.transaction_controller import TransactionController
from app.services.transaction_service import TransactionService
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter()

repository = TransactionRepository()
service = TransactionService(repository)
controller = TransactionController(service)

@router.get("/transactions", response_model=List[TransactionResponse])
def list_transactions(
    type: Optional[str] = Query(default=None),
    category_id: Optional[UUID] = Query(default=None),
    account_id: Optional[UUID] = Query(default=None),
):
    return controller.list_transactions(type=type, category_id=category_id, account_id=account_id)

@router.post("/transactions", response_model=TransactionResponse)
def create_transaction(data: TransactionCreate):
    return controller.create_transaction(data)