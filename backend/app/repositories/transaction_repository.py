from datetime import date
from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Reads ----------

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        type: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> List[Transaction]:
        offset = (page - 1) * page_size

        query = (
            self.db.query(Transaction)
            .options(
                joinedload(Transaction.account),
                joinedload(Transaction.category),
            )
        )

        query = self._apply_filters(
            query=query,
            type=type,
            date_from=date_from,
            date_to=date_to,
        )

        return (
            query
            .order_by(Transaction.created_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

    def list_by_account(
        self,
        account_id: UUID,
        page: int = 1,
        page_size: int = 20,
        type: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> List[Transaction]:
        offset = (page - 1) * page_size

        query = (
            self.db.query(Transaction)
            .options(
                joinedload(Transaction.account),
                joinedload(Transaction.items),
                joinedload(Transaction.category),
            )
            .filter(Transaction.account_id == account_id)
        )

        query = self._apply_filters(
            query=query,
            type=type,
            date_from=date_from,
            date_to=date_to,
        )

        return (
            query
            .order_by(Transaction.created_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

    def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        return (
            self.db.query(Transaction)
            .options(
                joinedload(Transaction.account),
                joinedload(Transaction.category),
            )
            .filter(Transaction.id == transaction_id)
            .first()
        )

    def count(
        self,
        type: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> int:
        query = self.db.query(Transaction)

        query = self._apply_filters(
            query=query,
            type=type,
            date_from=date_from,
            date_to=date_to,
        )

        return query.count()

    def count_by_account(
        self,
        account_id: UUID,
        type: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> int:
        query = (
            self.db.query(Transaction)
            .filter(Transaction.account_id == account_id)
        )

        query = self._apply_filters(
            query=query,
            type=type,
            date_from=date_from,
            date_to=date_to,
        )

        return query.count()

    # ---------- Writes ----------

    def create(self, data: TransactionCreate, user_id: UUID) -> Transaction:
        transaction = Transaction(
            account_id=data.account_id,
            category_id=data.category_id,
            subcategory_id=data.subcategory_id,
            store_id=data.store_id,
            city_id=data.city_id,
            paid_by=data.paid_by,
            paid_to=data.paid_to,
            payment_method=data.payment_method,
            type=data.type,
            amount=data.amount,
            description=data.description.strip() if data.description else None,
            date=data.date,
            created_by=user_id,
            updated_by=user_id,
        )

        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)

        if hasattr(data, "item_ids") and data.item_ids is not None:
            transaction.items = data.item_ids
            self.db.commit()
            self.db.refresh(transaction)

        return self.get_by_id(transaction.id)

    def update(self, transaction_id: UUID, data: TransactionUpdate, user_id: UUID) -> Optional[Transaction]:
        transaction = self.get_by_id(transaction_id)
        if not transaction:
            return None

        update_data = data.model_dump(exclude_unset=True)

        item_ids = update_data.pop("item_ids", None) if "item_ids" in update_data else None

        for field, value in update_data.items():
            if isinstance(value, str):
                value = value.strip()

            if field == "description" and value == "":
                value = None

            setattr(transaction, field, value)

        if item_ids is not None:
            transaction.items = item_ids

        transaction.updated_by = user_id

        self.db.commit()
        self.db.refresh(transaction)
        return self.get_by_id(transaction.id)

    def delete(self, transaction_id: UUID) -> bool:
        transaction = self.get_by_id(transaction_id)
        if not transaction:
            return False

        self.db.delete(transaction)
        self.db.commit()
        return True

    # ---------- Helpers ----------

    def _apply_filters(
        self,
        query,
        type: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ):
        if type is not None:
            normalized_type = type.strip().lower()
            query = query.filter(Transaction.type == TransactionType(normalized_type))

        if date_from is not None:
            query = query.filter(Transaction.date >= date_from)

        if date_to is not None:
            query = query.filter(Transaction.date <= date_to)

        return query