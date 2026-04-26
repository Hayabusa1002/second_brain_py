from uuid import UUID

from fastapi import UploadFile

from app.schemas.bulk_import import ImportResult
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.category_service import CategoryService


class CategoryController:
    def __init__(self, service: CategoryService):
        self.service = service

    # ---------- Reads ----------

    def list_categories(self):
        return self.service.list_categories()

    def get_category(self, category_id: UUID):
        return self.service.get_category(category_id)

    # ---------- Writes ----------

    def create_category(self, data: CategoryCreate, user_id: UUID):
        return self.service.create_category(data=data, user_id=user_id)

    def update_category(self, category_id: UUID, data: CategoryUpdate, user_id: UUID):
        return self.service.update_category(category_id=category_id, data=data, user_id=user_id)

    def delete_category(self, category_id: UUID, user_id: UUID) -> bool:
        return self.service.delete_category(category_id, user_id)

    # ---------- Bulk import ----------

    async def import_categories(self, file: UploadFile, current_user) -> ImportResult:
        return await self.service.import_categories(file=file, user_id=current_user.id)