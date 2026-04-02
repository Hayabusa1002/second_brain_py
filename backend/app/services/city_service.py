from uuid import UUID

from app.repositories.city_repository import CityRepository


class CityService:
    def __init__(self, repository: CityRepository):
        self.repository = repository

    def list_cities(self):
        return self.repository.list()

    def get_city(self, city_id: UUID):
        return self.repository.get_by_id(city_id)

    def create_city(self, data):
        existing = self.repository.get_by_name(data.name)
        if existing:
            return existing
        return self.repository.add(data)

    def update_city(self, city_id: UUID, data):
        return self.repository.update(city_id, data)