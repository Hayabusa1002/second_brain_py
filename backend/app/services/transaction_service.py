from uuid import UUID

from fastapi import UploadFile

from app.repositories.transaction_repository import TransactionRepository
from app.schemas.bulk_import import ImportResult
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.services.imports.transaction_import import TransactionImportService


class TransactionNotFoundError(Exception):
    def __init__(self, message: str = "Transaction not found"):
        super().__init__(message)


class TransactionService:
    def __init__(
        self,
        repository: TransactionRepository,
        import_service: TransactionImportService | None = None,
    ):
        self.repository = repository
        self.import_service = import_service

    # ---------- Reads ----------

    def list_transactions(self, page: int = 1, page_size: int = 20, account_id: UUID | None = None):
        if account_id is not None:
            items = self.repository.list_by_account(
                account_id=account_id,
                page=page,
                page_size=page_size,
            )
            total = self.repository.count_by_account(account_id)
            return items, total

        items = self.repository.list(page=page, page_size=page_size)
        total = self.repository.count()
        return items, total

    def get_transaction(self, transaction_id: UUID):
        transaction = self.repository.get_by_id(transaction_id)
        if not transaction:
            raise TransactionNotFoundError()
        return transaction

    # ---------- Writes ----------

    def create_transaction(self, data: TransactionCreate, user_id: UUID):
        create_data = self._build_create_data(data)
        return self.repository.create(data=create_data, user_id=user_id)

    def update_transaction(self, transaction_id: UUID, data: TransactionUpdate, user_id: UUID):
        self.get_transaction(transaction_id)
        update_data = data.model_dump(exclude_unset=True)

        if "description" in update_data and update_data["description"] is not None:
            update_data["description"] = update_data["description"].strip() or None

        if "paid_by" in update_data and "paid_to" not in update_data:
            update_data["paid_to"] = update_data["paid_by"]

        payload = TransactionUpdate(**update_data)

        updated = self.repository.update(
            transaction_id=transaction_id,
            data=payload,
            user_id=user_id,
        )
        if not updated:
            raise TransactionNotFoundError()
        return updated

    def delete_transaction(self, transaction_id: UUID) -> bool:
        self.get_transaction(transaction_id)
        return self.repository.delete(transaction_id)

    # ---------- Bulk import ----------

    async def import_transactions(self, file: UploadFile, user_id: UUID) -> ImportResult:
        return await self.import_service.import_file(file=file, user_id=user_id)

    # ---------- Helpers ----------

    def _build_create_data(self, data: TransactionCreate) -> TransactionCreate:
        return TransactionCreate(
            type=data.type,
            payment_method=data.payment_method,
            amount=data.amount,
            description=data.description.strip() if data.description else None,
            date=data.date,
            account_id=data.account_id,
            category_id=data.category_id,
            subcategory_id=data.subcategory_id,
            store_id=data.store_id,
            city_id=data.city_id,
            paid_by=data.paid_by,
            paid_to=data.paid_to or data.paid_by,
        )