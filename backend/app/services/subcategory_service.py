from uuid import UUID

from app.repositories.category_repository import CategoryRepository
from app.repositories.subcategory_repository import SubcategoryRepository
from app.schemas.subcategory import SubcategoryCreate, SubcategoryUpdate


class SubcategoryService:
    def __init__(
        self,
        repository: SubcategoryRepository,
        category_repository: CategoryRepository,
    ):
        self.repository = repository
        self.category_repository = category_repository

    def list_subcategories(self, category_id: UUID):
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return []
        return self.repository.list(category_id=category_id)

    def get_subcategory(self, category_id: UUID, subcategory_id: UUID):
        return self.repository.get_by_id_and_category(subcategory_id, category_id)

    def create_subcategory(self, category_id: UUID, data: SubcategoryCreate):
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return None

        existing = self.repository.get_by_name_and_category(data.name, category_id)
        if existing:
            return existing

        return self.repository.add(category_id=category_id, data=data)

    def update_subcategory(
        self,
        category_id: UUID,
        subcategory_id: UUID,
        data: SubcategoryUpdate,
    ):
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return None

        subcategory = self.repository.get_by_id_and_category(subcategory_id, category_id)
        if not subcategory:
            return None

        if getattr(data, "name", None):
            existing = self.repository.get_by_name_and_category(data.name, category_id)
            if existing and existing.id != subcategory_id:
                return None

        return self.repository.update(subcategory_id, data)

    def delete_subcategory(self, category_id: UUID, subcategory_id: UUID) -> bool:
        subcategory = self.repository.get_by_id_and_category(subcategory_id, category_id)
        if not subcategory:
            return False
        return self.repository.delete(subcategory_id)