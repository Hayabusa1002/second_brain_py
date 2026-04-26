from uuid import UUID

from fastapi import UploadFile

from app.schemas.bulk_import import ImportResult
from app.schemas.city import CityCreate, CityUpdate
from app.services.city_service import CityService


class CityController:
    def __init__(self, service: CityService):
        self.service = service

    # ---------- Reads ----------

    def list_cities(self):
        return self.service.list_cities()

    def get_city(self, city_id: UUID):
        return self.service.get_city(city_id)

    # ---------- Writes ----------

    def create_city(self, data: CityCreate, user_id: UUID):
        return self.service.create_city(data=data, user_id=user_id)

    def update_city(self, city_id: UUID, data: CityUpdate, user_id: UUID):
        return self.service.update_city(city_id=city_id, data=data, user_id=user_id)

    def delete_city(self, city_id: UUID) -> bool:
        return self.service.delete_city(city_id)

    # ---------- Bulk import ----------

    async def import_cities(self, file: UploadFile, current_user) -> ImportResult:
        return await self.service.import_cities(file=file, user_id=current_user.id)