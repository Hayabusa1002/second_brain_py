from fastapi import APIRouter
from typing import List

from app.controllers.transaction_controller import TransactionController
from app.services.transaction_service import TransactionService
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter()

repository = TransactionRepository()
service = TransactionService(repository)
controller = TransactionController(service)

@router.get("/transactions", response_model=List[TransactionResponse])
def list_transactions():
    return controller.list_transactions()

@router.post("/transactions", response_model=TransactionResponse)
def create_transaction(data: TransactionCreate):
    return controller.create_transaction(data)