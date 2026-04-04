from uuid import UUID

from app.repositories.subcategory_repository import SubcategoryRepository
from app.repositories.category_repository import CategoryRepository


class SubcategoryService:
    def __init__(self, repository: SubcategoryRepository, category_repository: CategoryRepository):
        self.repository = repository
        self.category_repository = category_repository

    def list_subcategories(self, category_id: UUID | None = None):
        return self.repository.list(category_id=category_id)

    def get_subcategory(self, subcategory_id: UUID):
        return self.repository.get_by_id(subcategory_id)

    def create_subcategory(self, data):
        category = self.category_repository.get_by_id(data.category_id)
        if not category:
            return None

        existing = self.repository.get_by_name_and_category(data.name, data.category_id)
        if existing:
            return existing

        return self.repository.add(data)

    def update_subcategory(self, subcategory_id: UUID, data):
        if getattr(data, "category_id", None):
            category = self.category_repository.get_by_id(data.category_id)
            if not category:
                return None

        return self.repository.update(subcategory_id, data)
    
    def delete_subcategory(self, subcategory_id: UUID) -> bool:
        return self.repository.delete(subcategory_id)