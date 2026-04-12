from uuid import UUID

from app.repositories.category_repository import CategoryRepository
from app.repositories.subcategory_repository import SubcategoryRepository
from app.schemas.subcategory import SubcategoryCreate, SubcategoryUpdate


class CategoryNotFoundError(Exception):
    def __init__(self, message: str = "Category not found"):
        super().__init__(message)


class SubcategoryNotFoundError(Exception):
    def __init__(self, message: str = "Subcategory not found"):
        super().__init__(message)


class DuplicateSubcategoryError(Exception):
    def __init__(self, name: str):
        super().__init__(f"Subcategory '{name}' already exists")


class SubcategoryService:
    def __init__(
        self,
        repository: SubcategoryRepository,
        category_repository: CategoryRepository,
    ):
        self.repository = repository
        self.category_repository = category_repository

    # ---------- Reads ----------

    def list_subcategories(self):
        return self.repository.list()

    def list_subcategories_by_category(self, category_id: UUID):
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError()
        return self.repository.list_by_category(category_id=category_id)
    
    def get_category(self, category_id: UUID):
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError()
        return category
    
    def get_subcategory(self, subcategory_id: UUID):
        subcategory = self.repository.get_by_id(subcategory_id)
        if not subcategory:
            raise SubcategoryNotFoundError()
        return subcategory
    
    def get_subcategory_by_name(self, subcategory_name: str):
        existing = self.repository.get_by_name(subcategory_name)
        if existing:
            raise DuplicateSubcategoryError(subcategory_name)
        return existing
    
    def get_subcategory_by_category(self, subcategory_id: UUID, category_id: UUID):
        self.get_category(category_id)
        subcategory = self.repository.get_by_id_and_category(subcategory_id, category_id)
        if not subcategory:
            raise SubcategoryNotFoundError()
        return subcategory

    # ---------- Writes ----------

    def create_subcategory(self, category_id: UUID, data: SubcategoryCreate, user_id: UUID):
        self.get_category(category_id)
        self.get_subcategory_by_name(data.name)
        return self.repository.create(data=data, user_id=user_id)

    def update_subcategory(self, category_id: UUID, subcategory_id: UUID, data: SubcategoryUpdate, user_id: UUID):
        self.get_subcategory_by_category(subcategory_id, category_id)
        if data.name is not None:
            self.get_subcategory_by_name(data.name)
        return self.repository.update(subcategory_id=subcategory_id, data=data, user_id=user_id)

    def delete_subcategory(self, category_id: UUID, subcategory_id: UUID) -> bool:
        self.get_subcategory_by_category(subcategory_id, category_id)
        return self.repository.delete(subcategory_id)