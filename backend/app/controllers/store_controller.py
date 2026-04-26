from uuid import UUID

from fastapi import UploadFile

from app.schemas.store import StoreCreate, StoreUpdate
from app.schemas.bulk_import import ImportResult
from app.services.store_service import StoreService


class StoreController:
    def __init__(self, service: StoreService):
        self.service = service

    # ---------- Reads ----------

    def list_stores(self):
        return self.service.list_stores()

    def get_store(self, store_id: UUID):
        return self.service.get_store(store_id)

    def list_store_subcategories(self, store_id: UUID):
        return self.service.list_store_subcategories(store_id)

    # ---------- Writes ----------

    def create_store(self, data: StoreCreate, user_id: UUID):
        return self.service.create_store(data=data, user_id=user_id)

    def update_store(self, store_id: UUID, data: StoreUpdate, user_id: UUID):
        return self.service.update_store(store_id=store_id, data=data, user_id=user_id)

    def delete_store(self, store_id: UUID, user_id: UUID):
        return self.service.delete_store(store_id=store_id, user_id=user_id)

    def replace_store_subcategories(self, store_id: UUID, subcategory_ids: list[UUID]):
        return self.service.replace_store_subcategories(
            store_id=store_id,
            subcategory_ids=subcategory_ids,
        )

    # ---------- Bulk import ----------

    async def import_stores(self, file: UploadFile, current_user) -> ImportResult:
        return await self.service.import_stores(file=file, user_id=current_user.id)