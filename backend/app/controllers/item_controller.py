from uuid import UUID

from fastapi import UploadFile

from app.schemas.bulk_import import ImportResult
from app.schemas.item import ItemCreate, ItemUpdate
from app.services.item_service import ItemService


class ItemController:
    def __init__(self, service: ItemService):
        self.service = service

    # ---------- Reads ----------

    def list_items(self):
        return self.service.list_items()

    def list_item_subcategories(self, item_id: UUID):
        return self.service.list_item_subcategories(item_id)

    def get_item(self, item_id: UUID):
        return self.service.get_item(item_id)

    # ---------- Writes ----------

    def create_item(self, data: ItemCreate, user_id: UUID):
        return self.service.create_item(data=data, user_id=user_id)

    def update_item(self, item_id: UUID, data: ItemUpdate, user_id: UUID):
        return self.service.update_item(item_id=item_id, data=data, user_id=user_id)

    def delete_item(self, item_id: UUID) -> bool:
        return self.service.delete_item(item_id)

    # ---------- Bulk import ----------

    async def import_items(self, file: UploadFile, current_user) -> ImportResult:
        return await self.service.import_items(file=file, user_id=current_user.id)