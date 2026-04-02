from uuid import UUID

from app.services.subcategory_service import SubcategoryService


class SubcategoryController:
    def __init__(self, service: SubcategoryService):
        self.service = service

    def list_subcategories(self, category_id: UUID | None = None):
        return self.service.list_subcategories(category_id=category_id)

    def get_subcategory(self, subcategory_id: UUID):
        return self.service.get_subcategory(subcategory_id)

    def create_subcategory(self, data):
        return self.service.create_subcategory(data)

    def update_subcategory(self, subcategory_id: UUID, data):
        return self.service.update_subcategory(subcategory_id, data)