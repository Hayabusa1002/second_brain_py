from typing import List, Optional
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session, joinedload

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
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        q: Optional[str] = None,
    ) -> List[Transaction]:
        query = (
            self.db.query(Transaction)
            .options(joinedload(Transaction.account), joinedload(Transaction.category))
            .filter(Transaction.created_by == user_id)
        )

        if type:
            query = query.filter(Transaction.type == type)
        if category_id:
            query = query.filter(Transaction.category_id == category_id)
        if account_id:
            query = query.filter(Transaction.account_id == account_id)
        if date_from:
            query = query.filter(Transaction.date >= date_from)
        if date_to:
            query = query.filter(Transaction.date <= date_to)
        if q:
            query = query.filter(Transaction.description.ilike(f"%{q}%"))

        return query.order_by(Transaction.date.desc()).all()

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
        tx.account_id   = data.account_id
        tx.category_id  = data.category_id
        tx.amount       = data.amount
        tx.type         = data.type
        tx.date         = data.date
        tx.description  = data.description
        self.db.commit()
        self.db.refresh(tx)
        return tx

    def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()

    def delete(self, transaction_id: UUID) -> bool:
        tx = self.get_by_id(transaction_id)
        if not tx:
            return False
        self.db.delete(tx)
        self.db.commit()
        return True