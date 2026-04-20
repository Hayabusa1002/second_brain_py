from uuid import UUID

from fastapi import UploadFile

from app.models.store import StoreType
from app.repositories.store_repository import StoreRepository
from app.schemas.store import StoreCreate, StoreUpdate, StoreSubcategoryAssign
from app.schemas.bulk_import import ImportResult
from app.services.imports.store_import import StoreImportService


class StoreNotFoundError(Exception):
    def __init__(self, message: str = "Store not found"):
        super().__init__(message)


class DuplicateStoreError(Exception):
    def __init__(self, name: str, store_type: str):
        super().__init__(f"Store '{name}' ({store_type}) already exists")


class StoreSubcategoriesNotFoundError(Exception):
    def __init__(self, message: str = "One or more subcategories were not found"):
        super().__init__(message)


class StoreService:
    def __init__(
        self,
        repository: StoreRepository,
        import_service: StoreImportService | None = None,
    ):
        self.repository = repository
        self.import_service = import_service

    # ---------- Reads ----------

    def list_stores(self):
        return self.repository.list()

    def list_store_subcategories(self, store_id: UUID):
        store = self.repository.get_by_id(store_id)
        if not store:
            raise StoreNotFoundError()
        return self.repository.list_subcategories(store_id)

    def get_store(self, store_id: UUID):
        store = self.repository.get_by_id(store_id)
        if not store:
            raise StoreNotFoundError()
        return store
    
    def get_store_by_identity(self, store_name: str, store_tpye: StoreType):
        existing = self.repository.get_by_name_and_type(store_name, store_tpye)
        if existing:
            raise DuplicateStoreError(store_name, store_tpye)
        return existing

    # ---------- Writes ----------

    def create_store(self, data: StoreCreate, user_id: UUID):
        self.get_store_by_identity(data.name, data.type)
        return self.repository.create(data=data, user_id=user_id)

    def update_store(self, store_id: UUID, data: StoreUpdate, user_id: UUID):
        store = self.get_store(store_id)
        if data.name is not None:
            store_type = data.type or store.type
            self.get_store_by_identity(data.name, store_type)
        return self.repository.update(store_id=store_id, data=data, user_id=user_id)

    def delete_store(self, store_id: UUID) -> bool:
        self.get_store(store_id)
        return self.repository.delete(store_id)

    # ---------- Subcategories assignation ----------

    def replace_store_subcategories(self, store_id: UUID, data: StoreSubcategoryAssign, user_id: UUID):
        self.get_store(store_id)
        unique_ids = list(dict.fromkeys(data.subcategory_ids))
        existing_subcategories = self.repository.get_subcategories_by_ids(unique_ids)
        if len(existing_subcategories) != len(unique_ids):
            raise StoreSubcategoriesNotFoundError()
        return self.repository.replace_subcategories(store_id=store_id, subcategory_ids=data.subcategory_ids, user_id=user_id)

    # ---------- Bulk import ----------

    async def import_stores(self, file: UploadFile, user_id: UUID) -> ImportResult:
        return await self.import_service.import_file(file=file, user_id=user_id)