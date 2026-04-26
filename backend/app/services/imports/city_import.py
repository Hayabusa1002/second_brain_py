from types import SimpleNamespace
from typing import Any
from uuid import UUID

from fastapi import UploadFile

from app.repositories.city_repository import CityRepository
from app.schemas.bulk_import import ImportError, ImportResult
from app.services.helpers.import_service import BulkImportCollector, BulkImportService


def _normalize_row(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {
            "name": "",
            "state": "",
            "country": "",
        }

    return {
        "name": str(item.get("name") or "").strip(),
        "state": str(item.get("state") or "").strip(),
        "country": str(item.get("country") or "").strip(),
    }


def _validate_row(item: dict[str, Any], row: int) -> list[ImportError]:
    errors: list[ImportError] = []

    name = item.get("name", "").strip()
    country = item.get("country", "").strip()

    if not name:
        errors.append(ImportError(row=row, error="City name is required."))

    if not country:
        errors.append(ImportError(row=row, error="Country is required."))

    return errors


class CityImportService:
    def __init__(
        self,
        repository: CityRepository,
        bulk_import_service: BulkImportService,
    ):
        self.repository = repository
        self.bulk_import_service = bulk_import_service

    async def import_file(self, file: UploadFile, user_id: UUID) -> ImportResult:
        raw_rows = await self.bulk_import_service.parse_file(file)
        rows = [_normalize_row(item) for item in raw_rows]

        collector = BulkImportCollector(total=len(rows))
        seen_cities: set[tuple[str, str | None, str | None]] = set()

        for index, item in enumerate(rows, start=1):
            collector.processed += 1
            self._import_city_row(
                item=item,
                row=index,
                user_id=user_id,
                seen_cities=seen_cities,
                collector=collector,
            )

        return collector.build()

    def _import_city_row(
        self,
        item: dict[str, Any],
        row: int,
        user_id: UUID,
        seen_cities: set[tuple[str, str | None, str | None]],
        collector: BulkImportCollector,
    ) -> None:
        row_errors = _validate_row(item, row)
        if row_errors:
            collector.add_row_errors(
                row_errors=row_errors,
                entity="city",
                name=item.get("name") or None,
            )
            return

        city_name = item["name"].strip()
        state = (item.get("state") or "").strip() or None
        country = (item.get("country") or "").strip() or None

        city_key = (
            city_name.lower(),
            state.lower() if state else None,
            country.lower() if country else None,
        )

        if city_key in seen_cities:
            collector.add_warning(
                row=row,
                entity="city",
                name=city_name,
                message=(
                    f"Duplicate city in file: '{city_name}' "
                    f"(state={state or '-'}, country={country or '-'})."
                ),
                count_as_skip=True,
                count_as_error=True,
            )
            return

        seen_cities.add(city_key)

        existing = self.repository.get_by_identity(
            name=city_name,
            state=state,
            country=country,
        )

        if existing:
            collector.add_warning(
                row=row,
                entity="city",
                name=city_name,
                message="City already exists. Using existing record.",
                count_as_skip=True,
            )
            return

        self.repository.create(
            data=SimpleNamespace(
                name=city_name,
                state=state,
                country=country,
            ),
            user_id=user_id,
        )

        collector.imported += 1
        collector.add_info(
            row=row,
            entity="city",
            name=city_name,
            message="City created.",
        )