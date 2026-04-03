import uuid
from typing import Optional
from uuid import UUID
from datetime import date

from app.models.transaction import Transaction, TransactionType, PaymentMethod
from app.repositories.transaction_repository import TransactionRepository


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def list_transactions(
        self,
        user_id: UUID,
        type: Optional[TransactionType] = None,
        payment_method: Optional[PaymentMethod] = None,
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
    ):
        return self.repository.list(
            user_id=user_id,
            type=type,
            payment_method=payment_method,
            category_id=category_id,
            subcategory_id=subcategory_id,
            account_id=account_id,
            store_id=store_id,
            city_id=city_id,
            paid_by=paid_by,
            paid_to=paid_to,
            date_from=date_from,
            date_to=date_to,
            q=q,
        )

    def create_transaction(self, data, created_by_id: UUID) -> Transaction:
        paid_by = getattr(data, "paid_by", None)
        paid_to = getattr(data, "paid_to", None) or paid_by

        transaction = Transaction(
            id=uuid.uuid4(),
            account_id=data.account_id,
            store_id=getattr(data, "store_id", None),
            category_id=data.category_id,
            subcategory_id=getattr(data, "subcategory_id", None),
            city_id=getattr(data, "city_id", None),
            amount=data.amount,
            type=data.type,
            payment_method=data.payment_method,
            description=getattr(data, "description", None),
            date=data.date,
            created_by=created_by_id,
            paid_by=paid_by,
            paid_to=paid_to,
        )
        return self.repository.add(transaction)

    def update(self, transaction_id: UUID, data, user_id: UUID) -> Optional[Transaction]:
        tx = self.get_by_id(transaction_id, user_id)
        if not tx:
            return None

        update_data = data.model_dump(exclude_unset=True)

        if "paid_by" in update_data and "paid_to" not in update_data:
            update_data["paid_to"] = update_data["paid_by"]

        for field, value in update_data.items():
            setattr(tx, field, value)

        self.repository.db.commit()
        self.repository.db.refresh(tx)
        return tx

    def get_by_id(self, transaction_id: UUID, user_id: UUID | None = None) -> Optional[Transaction]:
        tx = self.repository.get_by_id(transaction_id)
        if not tx:
            return None

        if user_id and tx.created_by != user_id:
            return None

        return tx

    def delete(self, transaction_id: UUID, user_id: UUID) -> bool:
        tx = self.get_by_id(transaction_id, user_id)
        if not tx:
            return False

        return self.repository.delete(transaction_id)