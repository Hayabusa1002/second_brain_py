from fastapi import APIRouter

from app.schemas.transaction import TransactionCreate
from app.services.transaction_service import TransactionService
from app.repositories.transaction_repository import TransactionRepository

router = APIRouter()

repository = TransactionRepository()
service = TransactionService(repository)

@router.get("/transactions")
def list_transactions():
    return service.list_transactions()

@router.post("/transactions")
def create_transaction(data: TransactionCreate):
    return service.create_transaction(data)