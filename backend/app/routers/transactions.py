from fastapi import APIRouter

from app.controllers.transaction_controller import TransactionController
from app.services.transaction_service import TransactionService
from app.repositories.transaction_repository import TransactionRepository

router = APIRouter()

repository = TransactionRepository()
service = TransactionService(repository)
controller = TransactionController(service)

@router.get("/transactions")
def list_transactions():
    return controller.list_transactions()

@router.post("/transactions")
def create_transaction(data):
    return controller.create_transaction(data)