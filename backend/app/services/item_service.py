from uuid import UUID

from fastapi import UploadFile

from app.repositories.item_repository import ItemRepository
from app.repositories.subcategory_repository import SubcategoryRepository
from app.schemas.item import ItemCreate, ItemUpdate
from app.schemas.bulk_import import ImportResult
from app.services.imports.item_import import ItemImportService


class ItemNotFoundError(Exception):
    def __init__(self, message: str = "Item not found"):
        super().__init__(message)


class DuplicateItemError(Exception):
    def __init__(self, name: str):
        super().__init__(f"Item '{name}' already exists")


class ItemSubcategoryNotFoundError(Exception):
    def __init__(self, message: str = "Subcategory not found"):
        super().__init__(message)


class ItemService:
    def __init__(
        self,
        repository: ItemRepository,
        subcategory_repository: SubcategoryRepository,
        import_service: ItemImportService | None = None,
    ):
        self.repository = repository
        self.subcategory_repository = subcategory_repository
        import_service = import_service

    # ---------- Reads ----------

    def list_items(self):
        return self.repository.list()
    
    def list_item_subcategories(self, item_id: UUID):
        item = self.repository.get_by_id(item_id)
        if not item:
            raise ItemNotFoundError()
        return self.repository.list_subcategories(item_id)

    def get_item(self, item_id: UUID):
        item = self.repository.get_by_id(item_id)
        if not item:
            raise ItemNotFoundError()
        return item
    
    def get_item_by_name(self, item_name: str):
        existing = self.repository.get_by_name(item_name)
        if existing:
            raise DuplicateItemError(item_name)
        return existing
    
    def get_item_subcategory(self, subcategory_id: UUID):
        subcategory = self.subcategory_repository.get_by_id(subcategory_id)
        if not subcategory:
            raise ItemSubcategoryNotFoundError()
    
    # ---------- Writes ----------

    def create_item(self, data: ItemCreate, user_id: UUID):
        self.get_item_by_name(data.name)
        if data.subcategory_id is not None:
            self.get_item_subcategory(data.subcategory_id)
        return self.repository.create(data=data, user_id=user_id)

    def update_item(self, item_id: UUID, data: ItemUpdate, user_id: UUID):
        self.get_item(item_id)
        if data.name is not None:
            self.get_item_by_name(data.name)
        if data.subcategory_id is not None:
            self.get_item_subcategory(data.subcategory_id)
        return self.repository.update(item_id=item_id, data=data, user_id=user_id)

    def delete_item(self, item_id: UUID) -> bool:
        self.get_item(item_id)
        return self.repository.delete(item_id)

    # ---------- Bulk import ----------

    async def import_items(self, file: UploadFile, user_id: UUID) -> ImportResult:
        return await self.import_service.import_file(file=file, user_id=user_id)