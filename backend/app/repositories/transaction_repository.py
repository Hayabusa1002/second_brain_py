from typing import List, Optional
from uuid import UUID
from app.models.transaction import Transaction

transactions_db: List[Transaction] = []
class TransactionRepository:
    def add(self, transaction: Transaction) -> Transaction:
        transactions_db.append(transaction)
        return transaction

    def list(self, type: Optional[str] = None, category_id: Optional[UUID] = None) -> List[Transaction]:
        result = transactions_db
        if type:
            result = [t for t in result if t.type == type]
        if category_id:
            result = [t for t in result if t.category_id == category_id]
        return result

    def get_by_account(self, account_id) -> List[Transaction]:
        return [t for t in transactions_db if t.account_id == account_id]