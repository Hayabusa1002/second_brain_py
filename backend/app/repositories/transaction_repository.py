from typing import List
from app.models.transaction import Transaction

transactions_db: List[Transaction] = []
class TransactionRepository:
    def add(self, transaction: Transaction) -> Transaction:
        transactions_db.append(transaction)
        return transaction

    def list(self) -> List[Transaction]:
        return transactions_db

    def get_by_account(self, account_id) -> List[Transaction]:
        return [
            t for t in transactions_db
            if t.account_id == account_id
        ]