from uuid import UUID

from app.schemas.subcategory import SubcategoryCreate, SubcategoryUpdate
from app.services.subcategory_service import SubcategoryService


class SubcategoryController:
    def __init__(self, service: SubcategoryService):
        self.service = service

    # ---------- Reads ----------

    def list_subcategories(self):
        return self.service.list_subcategories()

    def list_subcategories_by_category(self, category_id: UUID):
        return self.service.list_subcategories_by_category(category_id=category_id)

    def get_subcategory(self, subcategory_id: UUID):
        return self.service.get_subcategory(subcategory_id=subcategory_id)

    def get_subcategory_by_category(self, category_id: UUID, subcategory_id: UUID):
        return self.service.get_subcategory_by_category(
            subcategory_id=subcategory_id,
            category_id=category_id,
        )

    # ---------- Writes ----------

    def create_subcategory(self, category_id: UUID, data: SubcategoryCreate, user_id: UUID):
        return self.service.create_subcategory(
            category_id=category_id,
            data=data,
            user_id=user_id,
        )

    def update_subcategory(
        self,
        category_id: UUID,
        subcategory_id: UUID,
        data: SubcategoryUpdate,
        user_id: UUID,
    ):
        return self.service.update_subcategory(
            category_id=category_id,
            subcategory_id=subcategory_id,
            data=data,
            user_id=user_id,
        )

    def delete_subcategory(self, category_id: UUID, subcategory_id: UUID) -> bool:
        return self.service.delete_subcategory(
            category_id=category_id,
            subcategory_id=subcategory_id,
        )