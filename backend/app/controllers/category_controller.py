from uuid import UUID

from app.services.category_service import CategoryService


class CategoryController:
    def __init__(self, service: CategoryService):
        self.service = service

    def list_categories(self):
        return self.service.list_categories()

    def get_category(self, category_id: UUID):
        return self.service.get_category(category_id)

    def create_category(self, data):
        return self.service.create_category(data)

    def update_category(self, category_id: UUID, data):
        return self.service.update_category(category_id, data)