from typing import Any
from uuid import UUID

from fastapi import UploadFile

from app.models.store import StoreType
from app.repositories.store_repository import StoreRepository
from app.schemas.bulk_import import ImportError, ImportResult
from app.schemas.store import StoreCreate
from app.services.helpers.import_service import BulkImportCollector, BulkImportService


def _clean_value(value: Any) -> str | None:
    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip()
        return value or None

    text = str(value).strip()
    return text or None


def _normalize_row(row: Any) -> dict[str, Any]:
    if not isinstance(row, dict):
        return {
            "name": "",
            "type": "",
            "address": None,
            "website": None,
        }

    return {
        "name": _clean_value(row.get("name")) or "",
        "type": (_clean_value(row.get("type")) or "").lower(),
        "address": _clean_value(row.get("address")),
        "website": _clean_value(row.get("website")),
    }


def _safe_name(row: Any) -> str | None:
    if not isinstance(row, dict):
        return None

    value = row.get("name")
    if value is None:
        return None

    text = str(value).strip()
    return text or None


def _validate_row(item: dict[str, Any], row: int) -> list[ImportError]:
    errors: list[ImportError] = []

    name = (item.get("name") or "").strip()
    raw_type = (item.get("type") or "").strip().lower()

    if not name:
        errors.append(ImportError(row=row, error="Store name is required."))

    if not raw_type:
        errors.append(ImportError(row=row, error="Store type is required."))
    else:
        try:
            StoreType(raw_type)
        except ValueError:
            errors.append(
                ImportError(
                    row=row,
                    error=f"Invalid store type: '{raw_type}'.",
                )
            )

    return errors


class StoreImportService:
    def __init__(
        self,
        repository: StoreRepository,
        bulk_import_service: BulkImportService,
    ):
        self.repository = repository
        self.bulk_import_service = bulk_import_service

    async def import_file(self, file: UploadFile, user_id: UUID) -> ImportResult:
        raw_rows = await self.bulk_import_service.parse_file(file)
        rows = [_normalize_row(row) for row in raw_rows]

        collector = BulkImportCollector(total=len(rows))
        seen_stores: set[tuple[str, str]] = set()

        for index, item in enumerate(rows, start=1):
            collector.processed += 1
            self._import_store_row(
                item=item,
                raw_input=raw_rows[index - 1],
                row=index,
                user_id=user_id,
                seen_stores=seen_stores,
                collector=collector,
            )

        return collector.build()

    def _import_store_row(
        self,
        item: dict[str, Any],
        raw_input: Any,
        row: int,
        user_id: UUID,
        seen_stores: set[tuple[str, str]],
        collector: BulkImportCollector,
    ) -> None:
        try:
            row_errors = _validate_row(item, row)
            if row_errors:
                collector.add_row_errors(
                    row_errors=row_errors,
                    entity="store",
                    name=item.get("name") or None,
                )
                return

            store_name = item["name"].strip()
            raw_type = item["type"].strip().lower()
            store_type = StoreType(raw_type)

            store_key = (store_name.lower(), raw_type)
            if store_key in seen_stores:
                collector.add_warning(
                    row=row,
                    entity="store",
                    name=store_name,
                    message=f"Duplicate store in file: '{store_name}' ({raw_type}).",
                    count_as_skip=True,
                    count_as_error=True,
                )
                return

            seen_stores.add(store_key)

            existing = self.repository.get_by_name_and_type(store_name, store_type)
            if existing:
                collector.add_warning(
                    row=row,
                    entity="store",
                    name=store_name,
                    message="Store already exists. Using existing record.",
                    count_as_skip=True,
                )
                return

            store_data = StoreCreate(
                name=store_name,
                type=store_type,
                address=item.get("address"),
                website=item.get("website"),
            )

            self.repository.create(data=store_data, user_id=user_id)
            collector.imported += 1
            collector.add_info(
                row=row,
                entity="store",
                name=store_name,
                message="Store created.",
            )

        except Exception as exc:
            collector.add_error(
                row=row,
                entity="store",
                name=_safe_name(raw_input),
                message=str(exc),
            )