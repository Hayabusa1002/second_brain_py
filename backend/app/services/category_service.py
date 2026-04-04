from uuid import UUID

from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def list_categories(self):
        return self.repository.list()

    def get_category(self, category_id: UUID):
        return self.repository.get_by_id(category_id)

    def create_category(self, data):
        existing = self.repository.get_by_name(data.name)
        if existing:
            return existing
        return self.repository.add(data)

    def update_category(self, category_id: UUID, data):
        category = self.repository.get_by_id(category_id)
        if not category:
            return None

        if getattr(data, "name", None):
            existing = self.repository.get_by_name(data.name)
            if existing and existing.id != category_id:
                return None

        return self.repository.update(category_id, data)
    
    def delete_category(self, category_id: UUID) -> bool:
        return self.repository.delete(category_id)