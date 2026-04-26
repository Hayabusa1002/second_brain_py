import io
from decimal import Decimal, InvalidOperation
from uuid import UUID

import pandas as pd
from fastapi import UploadFile

from app.models.transaction import PaymentMethod, TransactionType
from app.repositories.account_repository import AccountRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.bulk_import import ImportError, ImportResult
from app.schemas.transaction import TransactionCreate


REQUIRED_COLUMNS = {"date", "amount", "type", "category", "account"}


class TransactionImportService:
    def __init__(
        self,
        repository: TransactionRepository,
        category_repository: CategoryRepository,
        account_repository: AccountRepository,
    ):
        self.repository = repository
        self.category_repository = category_repository
        self.account_repository = account_repository

    async def import_file(self, file: UploadFile, user_id: UUID) -> ImportResult:
        content = await file.read()
        filename = (file.filename or "").lower().strip()

        dataframe = self._read_file(content=content, filename=filename)
        dataframe.columns = dataframe.columns.str.lower().str.strip()

        missing_columns = REQUIRED_COLUMNS - set(dataframe.columns)
        if missing_columns:
            raise ValueError(f"Missing columns: {', '.join(sorted(missing_columns))}")

        imported = 0
        errors: list[ImportError] = []

        for index, row in dataframe.iterrows():
            row_number = index + 2
            error = self._import_row(row=row, row_number=row_number, user_id=user_id)

            if error:
                errors.append(error)
                continue

            imported += 1

        return ImportResult(
            total=len(dataframe),
            imported=imported,
            errors=errors,
        )

    # ---------- Helpers ----------

    def _read_file(self, content: bytes, filename: str) -> pd.DataFrame:
        if filename.endswith(".csv"):
            return pd.read_csv(io.BytesIO(content))

        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            return pd.read_excel(io.BytesIO(content))

        raise ValueError("Unsupported format. Use .csv or .xlsx")

    def _import_row(self, row, row_number: int, user_id: UUID) -> ImportError | None:
        try:
            transaction_date = pd.to_datetime(row["date"]).date()
        except Exception:
            return ImportError(
                row=row_number,
                error=f"Invalid date: '{row['date']}'. Expected YYYY-MM-DD",
            )

        try:
            amount = Decimal(str(row["amount"]))
            if amount <= 0:
                raise ValueError()
        except (InvalidOperation, ValueError):
            return ImportError(
                row=row_number,
                error=f"Amount must be a positive number: '{row['amount']}'",
            )

        raw_type = str(row["type"]).lower().strip()
        if raw_type not in ("income", "expense"):
            return ImportError(
                row=row_number,
                error=f"Type must be 'income' or 'expense': '{row['type']}'",
            )

        try:
            transaction_type = TransactionType(raw_type)
        except ValueError:
            return ImportError(
                row=row_number,
                error=f"Invalid transaction type: '{row['type']}'",
            )

        payment_method = self._parse_payment_method(row=row, row_number=row_number)
        if isinstance(payment_method, ImportError):
            return payment_method

        category_name = str(row["category"]).strip()
        category = self.category_repository.get_by_name(category_name)
        if not category:
            return ImportError(
                row=row_number,
                error=f"Category not found: '{row['category']}'",
            )

        if category.type.value != raw_type:
            return ImportError(
                row=row_number,
                error=f"Category '{row['category']}' is {category.type.value}, not {raw_type}",
            )

        account_name = str(row["account"]).strip()
        account = self.account_repository.get_by_name(account_name)
        if not account:
            return ImportError(
                row=row_number,
                error=f"Account not found: '{row['account']}'",
            )

        create_data = TransactionCreate(
            type=transaction_type,
            payment_method=payment_method,
            amount=amount,
            description=self._optional_str(row.get("description")),
            date=transaction_date,
            account_id=account.id,
            category_id=category.id,
            subcategory_id=None,
            store_id=None,
            city_id=None,
            paid_by=None,
            paid_to=None,
        )

        self.repository.create(data=create_data, user_id=user_id)
        return None

    def _parse_payment_method(self, row, row_number: int) -> PaymentMethod | ImportError:
        raw_payment_method = row.get("payment_method")

        if pd.isna(raw_payment_method) or not str(raw_payment_method).strip():
            return PaymentMethod.cash

        normalized = str(raw_payment_method).strip().lower()

        try:
            return PaymentMethod(normalized)
        except ValueError:
            return ImportError(
                row=row_number,
                error=f"Invalid payment_method: '{raw_payment_method}'",
            )

    def _optional_str(self, value) -> str | None:
        if value is None or pd.isna(value):
            return None

        value = str(value).strip()
        return value or None