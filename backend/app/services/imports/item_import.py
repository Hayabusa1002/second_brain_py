from typing import Any
from uuid import UUID

from fastapi import UploadFile

from app.repositories.item_repository import ItemRepository
from app.repositories.subcategory_repository import SubcategoryRepository
from app.schemas.bulk_import import ImportError, ImportResult
from app.schemas.item import ItemCreate
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
            "notes": None,
            "subcategory": None,
        }

    return {
        "name": _clean_value(row.get("name")) or "",
        "notes": _clean_value(row.get("notes")),
        "subcategory": _clean_value(row.get("subcategory")),
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
    if not name:
        errors.append(ImportError(row=row, error="Field 'name' is required."))

    return errors


class ItemImportService:
    def __init__(
        self,
        repository: ItemRepository,
        subcategory_repository: SubcategoryRepository,
        bulk_import_service: BulkImportService,
    ):
        self.repository = repository
        self.subcategory_repository = subcategory_repository
        self.bulk_import_service = bulk_import_service

    async def import_file(self, file: UploadFile, user_id: UUID) -> ImportResult:
        raw_rows = await self.bulk_import_service.parse_file(file)
        rows = [_normalize_row(row) for row in raw_rows]

        collector = BulkImportCollector(total=len(rows))
        seen_items: set[str] = set()

        for index, item in enumerate(rows, start=1):
            collector.processed += 1
            self._import_item_row(
                item=item,
                raw_input=raw_rows[index - 1],
                row=index,
                user_id=user_id,
                seen_items=seen_items,
                collector=collector,
            )

        return collector.build()

    def _import_item_row(
        self,
        item: dict[str, Any],
        raw_input: Any,
        row: int,
        user_id: UUID,
        seen_items: set[str],
        collector: BulkImportCollector,
    ) -> None:
        try:
            row_errors = _validate_row(item, row)
            if row_errors:
                collector.add_row_errors(
                    row_errors=row_errors,
                    entity="item",
                    name=item.get("name") or None,
                )
                return

            item_name = item["name"].strip()
            item_key = item_name.lower()

            if item_key in seen_items:
                collector.add_warning(
                    row=row,
                    entity="item",
                    name=item_name,
                    message="Duplicate item in file, skipped.",
                    count_as_skip=True,
                    count_as_error=True,
                )
                return

            seen_items.add(item_key)

            existing = self.repository.get_by_name(item_name)
            if existing:
                collector.add_warning(
                    row=row,
                    entity="item",
                    name=item_name,
                    message="Item already exists, skipped.",
                    count_as_skip=True,
                )
                return

            subcategory_id = None
            subcategory_name = item.get("subcategory")

            if subcategory_name:
                subcategory = self.subcategory_repository.get_by_name(subcategory_name)
                if not subcategory:
                    collector.add_error(
                        row=row,
                        entity="item",
                        name=item_name,
                        message=f"Subcategory '{subcategory_name}' not found.",
                    )
                    return
                subcategory_id = subcategory.id

            item_data = ItemCreate(
                name=item_name,
                notes=item.get("notes"),
                subcategory_id=subcategory_id,
            )

            self.repository.create(data=item_data, user_id=user_id)
            collector.imported += 1
            collector.add_info(
                row=row,
                entity="item",
                name=item_name,
                message="Item imported successfully.",
            )

        except Exception as exc:
            collector.add_error(
                row=row,
                entity="item",
                name=_safe_name(raw_input),
                message=str(exc),
            )