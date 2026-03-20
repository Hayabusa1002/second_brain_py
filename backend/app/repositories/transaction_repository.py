from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.transaction import Transaction

class TransactionRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        user_id: UUID,
        type: Optional[str] = None,
        category_id: Optional[UUID] = None,
        account_id: Optional[UUID] = None,
    ) -> List[Transaction]:
        query = self.db.query(Transaction).filter(Transaction.created_by == user_id)
        if type:
            query = query.filter(Transaction.type == type)
        if category_id:
            query = query.filter(Transaction.category_id == category_id)
        if account_id:
            query = query.filter(Transaction.account_id == account_id)
        return query.all()

    def add(self, transaction: Transaction) -> Transaction:
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
    
    def get_by_account(self, account_id: UUID) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.account_id == account_id).all()
    
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