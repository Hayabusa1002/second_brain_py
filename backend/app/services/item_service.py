from decimal import Decimal
from uuid import UUID

from app.models.item import TransactionItem
from app.repositories.item_repository import ItemRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.subcategory_repository import SubcategoryRepository
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    def __init__(
        self,
        item_repository: ItemRepository,
        transaction_repository: TransactionRepository,
        subcategory_repository: SubcategoryRepository,
    ):
        self.item_repository = item_repository
        self.transaction_repository = transaction_repository
        self.subcategory_repository = subcategory_repository
        self.db = item_repository.db

    def list_items(self, transaction_id: UUID, user_id: UUID):
        tx = self.transaction_repository.get_by_id(transaction_id)
        if not tx or tx.created_by != user_id:
            return None

        return self.item_repository.list_by_transaction(transaction_id)

    def create_item(self, transaction_id: UUID, data: ItemCreate, user_id: UUID):
        tx = self.transaction_repository.get_by_id(transaction_id)
        if not tx or tx.created_by != user_id:
            return None

        if data.subcategory_id is not None:
            sub = self.subcategory_repository.get_by_id(data.subcategory_id)
            if not sub:
                raise ValueError("Subcategory not found")

        quantity = Decimal(str(data.quantity))
        unit_price = Decimal(str(data.unit_price))
        subtotal = quantity * unit_price

        item = TransactionItem(
            transaction_id=transaction_id,
            subcategory_id=data.subcategory_id,
            name=data.name,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal,
            notes=data.notes,
        )

        created = self.item_repository.add(item)
        self._sync_transaction_amount(transaction_id)
        return created

    def update_item(
        self,
        transaction_id: UUID,
        item_id: UUID,
        data: ItemUpdate,
        user_id: UUID,
    ):
        tx = self.transaction_repository.get_by_id(transaction_id)
        if not tx or tx.created_by != user_id:
            return None

        item = self.item_repository.get_by_transaction_and_id(transaction_id, item_id)
        if not item:
            return None

        update_data = data.model_dump(exclude_unset=True)

        # Validar subcategory si viene en el payload
        if "subcategory_id" in update_data:
            subcategory_id = update_data["subcategory_id"]
            if subcategory_id is not None:
                sub = self.subcategory_repository.get_by_id(subcategory_id)
                if not sub:
                    raise ValueError("Subcategory not found")

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