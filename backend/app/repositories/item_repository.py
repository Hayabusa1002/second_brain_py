from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.item import TransactionItem


class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_transaction(self, transaction_id: UUID) -> List[TransactionItem]:
        return (
            self.db.query(TransactionItem)
            .filter(TransactionItem.transaction_id == transaction_id)
            .all()
        )

    def get_by_id(self, item_id: UUID) -> Optional[TransactionItem]:
        return self.db.query(TransactionItem).filter(TransactionItem.id == item_id).first()

    def get_by_transaction_and_id(self, transaction_id: UUID, item_id: UUID) -> Optional[TransactionItem]:
        return (
            self.db.query(TransactionItem)
            .filter(
                TransactionItem.transaction_id == transaction_id,
                TransactionItem.id == item_id,
            )
            .first()
        )

    def add(self, item: TransactionItem) -> TransactionItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: TransactionItem, data) -> TransactionItem:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(item, field, value)

        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: TransactionItem) -> None:
        self.db.delete(item)
        self.db.commit()