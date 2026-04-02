from uuid import UUID

from app.repositories.store_repository import StoreRepository


class StoreService:
    def __init__(self, repository: StoreRepository):
        self.repository = repository

    def list_stores(self):
        return self.repository.list()

    def get_store(self, store_id: UUID):
        return self.repository.get_by_id(store_id)

    def create_store(self, data):
        existing = self.repository.get_by_name(data.name)
        if existing:
            return existing
        return self.repository.add(data)

    def update_store(self, store_id: UUID, data):
        return self.repository.update(store_id, data)