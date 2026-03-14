import uuid
import io
import pandas as pd
from datetime import datetime, UTC
from decimal import Decimal, InvalidOperation
from typing import List
from uuid import UUID

from app.models.transaction import Transaction
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.account_repository import AccountRepository
from app.schemas.bulk_import import ImportError, ImportResult

REQUIRED_COLUMNS = {"date", "amount", "type", "category", "account"}

class ImportService:

    def __init__(
        self,
        transaction_repo: TransactionRepository,
        category_repo: CategoryRepository,
        account_repo: AccountRepository,
    ):
        self.transaction_repo = transaction_repo
        self.category_repo    = category_repo
        self.account_repo     = account_repo

    def import_file(self, content: bytes, filename: str, created_by_id: UUID) -> ImportResult:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(content))
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise ValueError("Unsupported format. Use .csv or .xlsx")

        df.columns = df.columns.str.lower().str.strip()
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")

        imported = 0
        errors: List[ImportError] = []

        for i, row in df.iterrows():
            row_num = i + 2
            error = self._import_row(row, row_num, created_by_id)
            if error:
                errors.append(error)
            else:
                imported += 1

        return ImportResult(total=len(df), imported=imported, errors=errors)

    def _import_row(self, row, row_num: int, created_by_id: UUID):
        try:
            date = pd.to_datetime(row["date"]).date()
        except Exception:
            return ImportError(row=row_num, error=f"Invalid date: '{row['date']}'. Expected YYYY-MM-DD")

        # Validate amount
        try:
            amount = Decimal(str(row["amount"]))
            if amount <= 0:
                raise ValueError()
        except (InvalidOperation, ValueError):
            return ImportError(row=row_num, error=f"Amount must be a positive number: '{row['amount']}'")

        # Validate type
        t_type = str(row["type"]).lower().strip()
        if t_type not in ("income", "expense"):
            return ImportError(row=row_num, error=f"Type must be 'income' or 'expense': '{row['type']}'")

        # Validate category
        category = self.category_repo.get_by_name(str(row["category"]))
        if not category:
            return ImportError(row=row_num, error=f"Category not found: '{row['category']}'")
        if category.type != t_type:
            return ImportError(row=row_num, error=f"Category '{row['category']}' is {category.type}, not {t_type}")

        # Validate account
        account = self.account_repo.get_by_name(str(row["account"]))
        if not account:
            return ImportError(row=row_num, error=f"Account not found: '{row['account']}'")

        # Optional description
        raw_desc = row.get("description", "")
        description = str(raw_desc) if pd.notna(raw_desc) and str(raw_desc).strip() else None

        self.transaction_repo.add(Transaction(
            id=uuid.uuid4(),
            account_id=account.id,
            category_id=category.id,
            created_by=created_by_id,
            amount=amount,
            type=t_type,
            date=date,
            created_at=datetime.now(UTC),
        ))

        # no error
        return None