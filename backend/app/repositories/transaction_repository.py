from typing import List
from app.models.transaction import Transaction

class TransactionRepository:
    def __init__(self):
        self._transactions: List[Transaction] = []

    def add(self, transaction: Transaction):
        self._transactions.append(transaction)
        return transaction

    def list(self):
        return self._transactions