from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError

from app.models.category import CategoryType
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.bulk_import import ImportResult
from app.services.imports.category_import import CategoryImportService


class CategoryNotFoundError(Exception):
    def __init__(self, message: str = "Category not found"):
        super().__init__(message)


class DuplicateCategoryError(Exception):
    def __init__(self, name: str, type: str):
        super().__init__(f"Category '{name}' ({type}) already exists")


class CategoryHasSubcategoriesError(Exception):
    def __init__(self, message: str = "Category has subcategories. Remove them first."):
        super().__init__(message)


class CategoryHasTransactionsError(Exception):
    def __init__(self, message: str = "Category has transactions. Remove them first."):
        super().__init__(message)


class CategoryInUseError(Exception):
    def __init__(self, message: str = "Category cannot be deleted because it is in use."):
        super().__init__(message)


class CategoryService:
    def __init__(
        self,
        repository: CategoryRepository,
        import_service: CategoryImportService | None = None,
    ):
        self.repository = repository
        self.import_service = import_service

    # ---------- Reads ----------

    def list_categories(self):
        return self.repository.list()

    def get_category(self, category_id: UUID):
        category = self.repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError()
        return category
    
    def get_category_by_identity(self, category_name: str, category_tpye: CategoryType):
        existing = self.repository.get_by_name_and_type(category_name, category_tpye)
        if existing:
            raise DuplicateCategoryError(category_name, category_tpye)
        return existing

    # ---------- Writes ----------

    def create_category(self, data: CategoryCreate, user_id: UUID):
        self.get_category_by_identity(data.name, data.type)
        return self.repository.create(data=data, user_id=user_id)

    def update_category(self, category_id: UUID, data: CategoryUpdate, user_id: UUID):
        category = self.get_category(category_id)
        if data.name is not None:
            category_type = data.type or category.type
            self.get_category_by_identity(data.name, category_type)
        return self.repository.update(category_id=category_id, data=data, user_id=user_id)

    def delete_category(self, category_id: UUID) -> bool:
        category = self.get_category(category_id)
        if category.subcategories:
            raise CategoryHasSubcategoriesError()
        if category.transactions:
            raise CategoryHasTransactionsError()
        try:
            return self.repository.delete(category_id)
        except IntegrityError:
            raise CategoryInUseError()

    # ---------- Bulk import ----------

    async def import_categories(self, file: UploadFile, user_id: UUID) -> ImportResult:
        return await self.import_service.import_file(file=file, user_id=user_id)