from uuid import UUID

from app.services.city_service import CityService


class CityController:
    def __init__(self, service: CityService):
        self.service = service

    def list_cities(self):
        return self.service.list_cities()

    def get_city(self, city_id: UUID):
        return self.service.get_city(city_id)

    def create_city(self, data):
        return self.service.create_city(data)

    def update_city(self, city_id: UUID, data):
        return self.service.update_city(city_id, data)