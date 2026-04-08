from uuid import UUID

from app.services.item_service import ItemService
from app.schemas.item import ItemCreate, ItemUpdate


class ItemController:
    def __init__(self, service: ItemService):
        self.service = service

    def list_items(self, transaction_id: UUID, user_id: UUID):
        return self.service.list_items(transaction_id, user_id) 

    def create_item(self, transaction_id: UUID, data: ItemCreate, user_id: UUID):
        return self.service.create_item(transaction_id, data, user_id)

    def update_item(self, transaction_id: UUID, item_id: UUID, data: ItemUpdate, user_id: UUID):
        return self.service.update_item(transaction_id, item_id, data, user_id)

    def delete_item(self, transaction_id: UUID, item_id: UUID, user_id: UUID):
        return self.service.delete_item(transaction_id, item_id, user_id)