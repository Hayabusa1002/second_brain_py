import uuid
from typing import Optional
from uuid import UUID
from app.models.transaction import Transaction
from app.repositories.transaction_repository import TransactionRepository

class TransactionService:

    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def list_transactions(self, user_id: UUID, type=None, category_id=None, account_id=None):
        return self.repository.list(user_id=user_id, type=type, category_id=category_id, account_id=account_id)
    
    def create_transaction(self, data, created_by_id: UUID) -> Transaction:
        transaction = Transaction(
            id=uuid.uuid4(),
            account_id=data.account_id,
            category_id=data.category_id,
            amount=data.amount,
            type=data.type,
            date=data.date,
            created_by=created_by_id
        )
        return self.repository.add(transaction)

    def update(self, transaction_id: UUID, data) -> Optional[Transaction]:
        tx = self.get_by_id(transaction_id)
        if not tx:
            return None
        tx.account_id  = data.account_id
        tx.category_id = data.category_id
        tx.amount      = data.amount
        tx.type        = data.type
        tx.date        = data.date
        tx.description = data.description
        self.db.commit()
        self.db.refresh(tx)
        return tx

    def delete(self, transaction_id: UUID) -> bool:
        tx = self.get_by_id(transaction_id)
        if not tx:
            return False
        self.db.delete(tx)
        self.db.commit()
        return True