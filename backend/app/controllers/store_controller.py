from uuid import UUID

from fastapi import UploadFile

from app.services.store_service import StoreService
from app.schemas.store import StoreCreate, StoreUpdate


class StoreController:
    def __init__(self, service: StoreService):
        self.service = service

    def list_stores(self):
        return self.service.list_stores()

    def get_store(self, store_id: UUID):
        return self.service.get_store(store_id)

    def create_store(self, data: StoreCreate):
        return self.service.create_store(data)

    def update_store(self, store_id: UUID, data: StoreUpdate):
        return self.service.update_store(store_id, data)

    def delete_store(self, store_id: UUID):
        return self.service.delete_store(store_id)

    def list_store_subcategories(self, store_id: UUID):
        return self.service.list_store_subcategories(store_id)

    def replace_store_subcategories(self, store_id: UUID, subcategory_ids: list[UUID]):
        return self.service.replace_store_subcategories(store_id, subcategory_ids)

    async def import_stores(self, file: UploadFile, current_user=None):
        return await self.service.import_stores(file, current_user)