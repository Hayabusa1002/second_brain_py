import uuid
from datetime import datetime, UTC
from typing import Optional
from uuid import UUID
from app.models.transaction import Transaction
from app.repositories.transaction_repository import TransactionRepository
class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def create_transaction(self, data) -> Transaction:
        transaction = Transaction(
            id=uuid.uuid4(),
            account_id=data.account_id,
            category_id=data.category_id,
            amount=data.amount,
            type=data.type,
            date=data.date,
            created_at=datetime.now(UTC),
        )
        return self.repository.add(transaction)

    def list_transactions(
        self,
        type: Optional[str] = None,
        category_id: Optional[UUID] = None,
        account_id: Optional[UUID] = None,
    ):
        return self.repository.list(type=type, category_id=category_id, account_id=account_id)