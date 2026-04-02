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
        subcategory_id: Optional[UUID] = None,
        account_id: Optional[UUID] = None,
        store_id: Optional[UUID] = None,
        city_id: Optional[UUID] = None,
        paid_by: Optional[UUID] = None,
        paid_to: Optional[UUID] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        q: Optional[str] = None,
    ) -> List[Transaction]:
        query = (
            self.db.query(Transaction)
            .options(
                joinedload(Transaction.account),
                joinedload(Transaction.category),
                joinedload(Transaction.subcategory),
                joinedload(Transaction.store),
                joinedload(Transaction.city),
                joinedload(Transaction.creator),
                joinedload(Transaction.payer),
                joinedload(Transaction.payee),
            )
            .filter(Transaction.created_by == user_id)
        )

        if type:
            query = query.filter(Transaction.type == type)
        if category_id:
            query = query.filter(Transaction.category_id == category_id)
        if subcategory_id:
            query = query.filter(Transaction.subcategory_id == subcategory_id)
        if account_id:
            query = query.filter(Transaction.account_id == account_id)
        if store_id:
            query = query.filter(Transaction.store_id == store_id)
        if city_id:
            query = query.filter(Transaction.city_id == city_id)
        if paid_by:
            query = query.filter(Transaction.paid_by == paid_by)
        if paid_to:
            query = query.filter(Transaction.paid_to == paid_to)
        if date_from:
            query = query.filter(Transaction.date >= date_from)
        if date_to:
            query = query.filter(Transaction.date <= date_to)
        if q:
            query = query.filter(Transaction.description.ilike(f"%{q}%"))

        return query.order_by(Transaction.date.desc(), Transaction.created_at.desc()).all()

    def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        return (
            self.db.query(Transaction)
            .options(
                joinedload(Transaction.account),
                joinedload(Transaction.category),
                joinedload(Transaction.subcategory),
                joinedload(Transaction.store),
                joinedload(Transaction.city),
                joinedload(Transaction.creator),
                joinedload(Transaction.payer),
                joinedload(Transaction.payee),
                joinedload(Transaction.items),
            )
            .filter(Transaction.id == transaction_id)
            .first()
        )

    def get_by_account(self, account_id: UUID) -> List[Transaction]:
        return (
            self.db.query(Transaction)
            .filter(Transaction.account_id == account_id)
            .order_by(Transaction.date.desc(), Transaction.created_at.desc())
            .all()
        )

    def add(self, transaction: Transaction) -> Transaction:
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def update(self, transaction_id: UUID, data) -> Optional[Transaction]:
        tx = self.get_by_id(transaction_id)
        if not tx:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(tx, field, value)

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