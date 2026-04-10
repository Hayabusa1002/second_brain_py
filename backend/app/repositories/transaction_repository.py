from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Reads ----------

    def list(self, page: int = 1, page_size: int = 20) -> list[Transaction]:
        offset = (page - 1) * page_size

        return (
            self.db.query(Transaction)
            .options(
                joinedload(Transaction.account),
                joinedload(Transaction.category),
            )
            .order_by(Transaction.created_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

    def list_by_account(self, account_id: UUID, page: int = 1, page_size: int = 20) -> list[Transaction]:
        offset = (page - 1) * page_size

        return (
            self.db.query(Transaction)
            .options(
                joinedload(Transaction.account),
                joinedload(Transaction.items),
            )
            .filter(Transaction.account_id == account_id)
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

    def count(self) -> int:
        return self.db.query(Transaction).count()

    def count_by_account(self, account_id: UUID) -> int:
        return (
            self.db.query(Transaction)
            .filter(Transaction.account_id == account_id)
            .count()
        )


    # ---------- Writes ----------

    def create(self, data: TransactionCreate, user_id: UUID) -> Transaction:
        transaction = Transaction(
            account_id=data.account_id,
            type=data.type,
            amount=data.amount,
            description=data.description.strip() if data.description else None,
            transaction_date=data.transaction_date,
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