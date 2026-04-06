from uuid import UUID

from app.schemas.subcategory import SubcategoryCreate, SubcategoryUpdate
from app.services.subcategory_service import SubcategoryService


class SubcategoryController:
    def __init__(self, service: SubcategoryService):
        self.service = service

    def list_subcategories(self, category_id: UUID):
        return self.service.list_subcategories(category_id)

    def get_subcategory(self, category_id: UUID, subcategory_id: UUID):
        return self.service.get_subcategory(category_id, subcategory_id)

    def create_subcategory(self, category_id: UUID, data: SubcategoryCreate):
        return self.service.create_subcategory(category_id, data)

    def update_subcategory(
        self,
        category_id: UUID,
        subcategory_id: UUID,
        data: SubcategoryUpdate,
    ):
        return self.service.update_subcategory(category_id, subcategory_id, data)

    def delete_subcategory(self, category_id: UUID, subcategory_id: UUID) -> bool:
        return self.service.delete_subcategory(category_id, subcategory_id)