from typing import Any
from uuid import UUID

from fastapi import UploadFile

from app.models.category import CategoryType
from app.repositories.category_repository import CategoryRepository
from app.repositories.subcategory_repository import SubcategoryRepository
from app.schemas.bulk_import import ImportError, ImportResult
from app.schemas.category import CategoryCreate
from app.schemas.subcategory import SubcategoryCreate
from app.services.helpers.import_service import BulkImportCollector, BulkImportService


def _split_subcategory_names(value: Any) -> list[str]:
    if value is None:
        return []

    text = str(value).strip()
    if not text:
        return []

    return [part.strip() for part in text.split("|") if part and part.strip()]


def _normalize_row(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {
            "name": "",
            "type": "",
            "subcategories": [],
        }

    raw_subcategories = (
        item.get("subcategories")
        if "subcategories" in item
        else item.get("subcategory_names")
    )

    normalized_subcategories: list[str] = []

    if isinstance(raw_subcategories, list):
        for sub in raw_subcategories:
            if isinstance(sub, dict):
                normalized_subcategories.append(str(sub.get("name") or "").strip())
            else:
                normalized_subcategories.append(str(sub).strip())
    elif raw_subcategories is not None:
        normalized_subcategories = _split_subcategory_names(raw_subcategories)

    return {
        "name": str(item.get("name") or "").strip(),
        "type": str(item.get("type") or "").strip().lower(),
        "subcategories": normalized_subcategories,
    }


def _validate_row(item: dict[str, Any], row: int) -> list[ImportError]:
    errors: list[ImportError] = []

    name = item.get("name", "").strip()
    category_type = item.get("type", "").strip().lower()
    subcategories = item.get("subcategories", [])

    if not name:
        errors.append(ImportError(row=row, error="Category name is required."))

    if not category_type:
        errors.append(ImportError(row=row, error="Category type is required."))
    else:
        try:
            CategoryType(category_type)
        except ValueError:
            errors.append(
                ImportError(
                    row=row,
                    error="Category type must be 'income' or 'expense'.",
                )
            )

    if not isinstance(subcategories, list):
        errors.append(
            ImportError(
                row=row,
                error="Subcategories must be a list.",
            )
        )

    return errors


class CategoryImportService:
    def __init__(
        self,
        repository: CategoryRepository,
        subcategory_repository: SubcategoryRepository,
        bulk_import_service: BulkImportService,
    ):
        self.repository = repository
        self.subcategory_repository = subcategory_repository
        self.bulk_import_service = bulk_import_service

    async def import_file(self, file: UploadFile, user_id: UUID) -> ImportResult:
        raw_rows = await self.bulk_import_service.parse_file(file)
        rows = [_normalize_row(item) for item in raw_rows]

        collector = BulkImportCollector(total=len(rows))
        seen_categories: set[tuple[str, str]] = set()

        for index, item in enumerate(rows, start=1):
            collector.processed += 1
            self._import_category_row(
                item=item,
                row=index,
                user_id=user_id,
                seen_categories=seen_categories,
                collector=collector,
            )

        return collector.build()

    def _import_category_row(
        self,
        item: dict[str, Any],
        row: int,
        user_id: UUID,
        seen_categories: set[tuple[str, str]],
        collector: BulkImportCollector,
    ) -> None:
        row_errors = _validate_row(item, row)
        if row_errors:
            collector.add_row_errors(
                row_errors=row_errors,
                entity="category",
                name=item.get("name") or None,
            )
            return

        category_name = item["name"].strip()
        category_type = item["type"].strip().lower()
        category_key = (category_name.lower(), category_type)

        if category_key in seen_categories:
            collector.add_warning(
                row=row,
                entity="category",
                name=category_name,
                message=f"Duplicate category in file: '{category_name}' ({category_type}).",
                count_as_skip=True,
                count_as_error=True,
            )
            return

        seen_categories.add(category_key)

        category = self.repository.get_by_name_and_type(category_name, category_type)
        if not category:
            category = self.repository.create(
                data=CategoryCreate(
                    name=category_name,
                    type=CategoryType(category_type),
                ),
                user_id=user_id,
            )
            collector.imported += 1
            collector.add_info(
                row=row,
                entity="category",
                name=category_name,
                message="Category created.",
            )
        else:
            collector.add_warning(
                row=row,
                entity="category",
                name=category_name,
                message="Category already exists. Using existing record.",
                count_as_skip=True,
            )

        self._import_subcategories(
            row=row,
            category=category,
            category_name=category_name,
            subcategories=item.get("subcategories", []),
            user_id=user_id,
            collector=collector,
        )

    def _import_subcategories(
        self,
        row: int,
        category: Any,
        category_name: str,
        subcategories: list[str],
        user_id: UUID,
        collector: BulkImportCollector,
    ) -> None:
        seen_subcategories: set[str] = set()

        for sub_name in subcategories:
            normalized_sub_name = sub_name.strip()

            if not normalized_sub_name:
                collector.add_error(
                    row=row,
                    entity="subcategory",
                    message=f"Empty subcategory name in category '{category_name}'.",
                )
                continue

            sub_key = normalized_sub_name.lower()
            if sub_key in seen_subcategories:
                collector.add_warning(
                    row=row,
                    entity="subcategory",
                    name=normalized_sub_name,
                    message=f"Duplicate subcategory '{normalized_sub_name}' in category '{category_name}'.",
                    count_as_error=True,
                )
                continue

            seen_subcategories.add(sub_key)

            existing_sub = self.subcategory_repository.get_by_name_and_category(
                normalized_sub_name,
                category.id,
            )
            if existing_sub:
                collector.add_warning(
                    row=row,
                    entity="subcategory",
                    name=normalized_sub_name,
                    message="Subcategory already exists. Using existing record.",
                )
                continue

            self.subcategory_repository.create(
                category_id=category.id,
                data=SubcategoryCreate(name=normalized_sub_name),
                user_id=user_id,
            )
            collector.add_info(
                row=row,
                entity="subcategory",
                name=normalized_sub_name,
                message="Subcategory created.",
            )