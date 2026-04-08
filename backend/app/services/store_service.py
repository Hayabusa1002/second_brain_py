import csv
import io
import json
from typing import List
from uuid import UUID

import pandas as pd
import yaml
from fastapi import UploadFile

from app.repositories.store_repository import StoreRepository
from app.schemas.store import (
    StoreCreate,
    StoreUpdate,
    StoreSubcategoryLinkResponse,
)
from app.schemas.bulk_import import ImportResult, ImportError, ImportLogItem


class StoreService:
    VALID_EXTENSIONS = (".csv", ".xlsx", ".xls", ".json", ".yaml", ".yml")

    def __init__(self, repository: StoreRepository):
        self.repository = repository

    def list_stores(self):
        return self.repository.list()

    def get_store(self, store_id: UUID):
        return self.repository.get_by_id(store_id)

    def create_store(self, data: StoreCreate):
        existing = self.repository.get_by_name(data.name)
        if existing:
            return existing
        return self.repository.add(data)

    def update_store(self, store_id: UUID, data: StoreUpdate):
        return self.repository.update(store_id, data)

    def delete_store(self, store_id: UUID):
        return self.repository.delete(store_id)

    def list_store_subcategories(self, store_id: UUID) -> List[StoreSubcategoryLinkResponse]:
        store = self.repository.get_by_id(store_id)
        if not store:
            raise ValueError("Store not found")

        links = self.repository.list_store_subcategories(store_id)
        return [
            StoreSubcategoryLinkResponse(
                id=link.id,
                store_id=link.store_id,
                subcategory_id=link.subcategory_id,
                created_at=link.created_at,
                subcategory=link.subcategory,
            )
            for link in links
        ]

    def replace_store_subcategories(
        self,
        store_id: UUID,
        subcategory_ids: List[UUID],
    ) -> List[StoreSubcategoryLinkResponse]:
        store = self.repository.get_by_id(store_id)
        if not store:
            raise ValueError("Store not found")

        unique_ids = list(dict.fromkeys(subcategory_ids))
        subcategories = self.repository.get_subcategories_by_ids(unique_ids)

        if len(subcategories) != len(unique_ids):
            raise ValueError("One or more subcategories were not found")

        links = self.repository.replace_store_subcategories(store_id, unique_ids)

        return [
            StoreSubcategoryLinkResponse(
                id=link.id,
                store_id=link.store_id,
                subcategory_id=link.subcategory_id,
                created_at=link.created_at,
                subcategory=link.subcategory,
            )
            for link in links
        ]

    async def import_stores(self, file: UploadFile, current_user=None) -> ImportResult:
        result = ImportResult()
        filename = (file.filename or "").lower()

        rows = await self._parse_file(file, filename)
        result.total = len(rows)

        for index, raw_row in enumerate(rows, start=1):
            result.processed += 1

            try:
                normalized = self._normalize_row(raw_row)
                store_data = StoreCreate(**normalized)

                existing = self.repository.get_by_name(store_data.name)
                if existing:
                    result.skipped += 1
                    result.logs.append(
                        ImportLogItem(
                            row=index,
                            level="warning",
                            entity="file",
                            name=store_data.name,
                            message="Store already exists, skipped.",
                        )
                    )
                    result.warnings += 1
                    continue

                self.repository.add(store_data)
                result.imported += 1
                result.logs.append(
                    ImportLogItem(
                        row=index,
                        level="info",
                        entity="file",
                        name=store_data.name,
                        message="Store imported successfully.",
                    )
                )

            except Exception as e:
                result.errors_count += 1
                result.errors.append(
                    ImportError(
                        row=index,
                        error=str(e),
                    )
                )
                result.logs.append(
                    ImportLogItem(
                        row=index,
                        level="error",
                        entity="file",
                        name=self._safe_name(raw_row),
                        message=str(e),
                    )
                )

        return result

    async def _parse_file(self, file: UploadFile, filename: str) -> list[dict]:
        content = await file.read()

        if filename.endswith(".csv"):
            text = content.decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(text))
            return [dict(row) for row in reader]

        if filename.endswith(".json"):
            data = json.loads(content.decode("utf-8"))
            if not isinstance(data, list):
                raise ValueError("JSON file must contain a list of stores.")
            return data

        if filename.endswith(".yaml") or filename.endswith(".yml"):
            data = yaml.safe_load(content.decode("utf-8"))
            if not isinstance(data, list):
                raise ValueError("YAML file must contain a list of stores.")
            return data

        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(io.BytesIO(content))
            df = df.where(pd.notnull(df), None)
            return df.to_dict(orient="records")

        raise ValueError("Unsupported format. Use CSV, XLSX, JSON or YAML.")

    def _normalize_row(self, row: dict) -> dict:
        name = self._clean_value(row.get("name"))
        store_type = self._clean_value(row.get("type"))
        address = self._clean_value(row.get("address"))
        website = self._clean_value(row.get("website"))

        if not name:
            raise ValueError("Field 'name' is required.")

        if not store_type:
            raise ValueError("Field 'type' is required.")

        return {
            "name": name,
            "type": store_type,
            "address": address,
            "website": website,
        }

    def _clean_value(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value

    def _safe_name(self, row: dict) -> str | None:
        if not isinstance(row, dict):
            return None
        value = row.get("name")
        if value is None:
            return None
        return str(value).strip() or None