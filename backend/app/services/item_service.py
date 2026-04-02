from decimal import Decimal
from uuid import UUID

from app.models.item import TransactionItem
from app.repositories.item_repository import ItemRepository
from app.repositories.transaction_repository import TransactionRepository


class ItemService:
    def __init__(self, db):
        self.db = db
        self.item_repository = ItemRepository(db)
        self.transaction_repository = TransactionRepository(db)

    def list_items(self, transaction_id: UUID, user_id: UUID):
        tx = self.transaction_repository.get_by_id(transaction_id)
        if not tx or tx.created_by != user_id:
            return None

        return self.item_repository.list_by_transaction(transaction_id)

    def create_item(self, transaction_id: UUID, data, user_id: UUID):
        tx = self.transaction_repository.get_by_id(transaction_id)
        if not tx or tx.created_by != user_id:
            return None

        quantity = Decimal(str(data.quantity))
        unit_price = Decimal(str(data.unit_price))
        subtotal = quantity * unit_price

        item = TransactionItem(
            transaction_id=transaction_id,
            name=data.name,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal,
            notes=data.notes,
        )

        created = self.item_repository.add(item)
        self._sync_transaction_amount(transaction_id)
        return created

    def update_item(self, transaction_id: UUID, item_id: UUID, data, user_id: UUID):
        tx = self.transaction_repository.get_by_id(transaction_id)
        if not tx or tx.created_by != user_id:
            return None

        item = self.item_repository.get_by_transaction_and_id(transaction_id, item_id)
        if not item:
            return None

        update_data = data.model_dump(exclude_unset=True)

        quantity = Decimal(str(update_data.get("quantity", item.quantity)))
        unit_price = Decimal(str(update_data.get("unit_price", item.unit_price)))

        update_data["subtotal"] = quantity * unit_price

        for field, value in update_data.items():
            setattr(item, field, value)

        self.db.commit()
        self.db.refresh(item)

        self._sync_transaction_amount(transaction_id)
        return item

    def delete_item(self, transaction_id: UUID, item_id: UUID, user_id: UUID):
        tx = self.transaction_repository.get_by_id(transaction_id)
        if not tx or tx.created_by != user_id:
            return False

        item = self.item_repository.get_by_transaction_and_id(transaction_id, item_id)
        if not item:
            return False

        self.item_repository.delete(item)
        self._sync_transaction_amount(transaction_id)
        return True

    def _sync_transaction_amount(self, transaction_id: UUID):
        tx = self.transaction_repository.get_by_id(transaction_id)
        if not tx:
            return

        items = self.item_repository.list_by_transaction(transaction_id)
        if items:
            tx.amount = sum((item.subtotal for item in items), Decimal("0.00"))
            self.db.commit()
            self.db.refresh(tx)