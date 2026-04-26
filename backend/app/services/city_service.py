from uuid import UUID

from fastapi import UploadFile

from app.repositories.city_repository import CityRepository
from app.schemas.city import CityCreate, CityUpdate
from app.schemas.bulk_import import ImportResult
from app.services.imports.city_import import CityImportService


class CityNotFoundError(Exception):
    def __init__(self, message: str = "City not found"):
        super().__init__(message)


class DuplicateCityError(Exception):
    def __init__(self, name: str, state: str | None, country: str | None):
        state_display = state or "-"
        country_display = country or "-"
        super().__init__(f"City '{name}' ({state_display}, {country_display}) already exists")


class CityService:
    def __init__(
        self,
        repository: CityRepository,
        import_service: CityImportService | None = None,
    ):
        self.repository = repository
        self.import_service = import_service

    # ---------- Reads ----------

    def list_cities(self):
        return self.repository.list()

    def get_city(self, city_id: UUID):
        city = self.repository.get_by_id(city_id)
        if not city:
            raise CityNotFoundError()
        return city

    def get_city_by_identity(
        self,
        city_name: str,
        state: str | None = None,
        country: str | None = None,
        exclude_id: UUID | None = None,
    ):
        existing = self.repository.get_by_identity(
            name=city_name,
            state=state,
            country=country,
        )
        if existing and existing.id != exclude_id:
            raise DuplicateCityError(city_name, state, country)

        return existing

    # ---------- Writes ----------

    def create_city(self, data: CityCreate, user_id: UUID):
        self.get_city_by_identity(data.name, data.state, data.country)
        return self.repository.create(data=data, user_id=user_id)

    def update_city(self, city_id: UUID, data: CityUpdate, user_id: UUID):
        city = self.get_city(city_id)

        new_name = data.name if data.name is not None else city.name
        new_state = data.state if data.state is not None else city.state
        new_country = data.country if data.country is not None else city.country

        self.get_city_by_identity(
            city_name=new_name,
            state=new_state,
            country=new_country,
            exclude_id=city_id,
        )

        return self.repository.update(city_id=city_id, data=data, user_id=user_id)

    def delete_city(self, city_id: UUID) -> bool:
        self.get_city(city_id)
        return self.repository.delete(city_id)

    # ---------- Bulk import ----------

    async def import_cities(self, file: UploadFile, user_id: UUID) -> ImportResult:
        return await self.import_service.import_file(file=file, user_id=user_id)