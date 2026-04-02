from uuid import UUID

from app.services.store_service import StoreService


class StoreController:
    def __init__(self, service: StoreService):
        self.service = service

    def list_stores(self):
        return self.service.list_stores()

    def get_store(self, store_id: UUID):
        return self.service.get_store(store_id)

    def create_store(self, data):
        return self.service.create_store(data)

    def update_store(self, store_id: UUID, data):
        return self.service.update_store(store_id, data)