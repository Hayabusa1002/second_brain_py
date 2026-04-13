from typing import Tuple
from uuid import UUID

from fastapi import UploadFile

from app.schemas.bulk_import import ImportResult
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.services.transaction_service import TransactionService


class TransactionController:
    def __init__(self, service: TransactionService):
        self.service = service

    # ---------- Reads ----------

    def list_transactions(
        self,
        page: int = 1,
        page_size: int = 20,
        account_id: UUID | None = None,
    ) -> Tuple[list, int]:
        return self.service.list_transactions(
            page=page,
            page_size=page_size,
            account_id=account_id,
        )

    def get_transaction(self, transaction_id: UUID):
        return self.service.get_transaction(transaction_id)

    # ---------- Writes ----------

    def create_transaction(self, data: TransactionCreate, user_id: UUID):
        return self.service.create_transaction(data=data, user_id=user_id)

    def update_transaction(
        self,
        transaction_id: UUID,
        data: TransactionUpdate,
        user_id: UUID,
    ):
        return self.service.update_transaction(
            transaction_id=transaction_id,
            data=data,
            user_id=user_id,
        )

    def delete_transaction(self, transaction_id: UUID) -> bool:
        return self.service.delete_transaction(transaction_id)

    # ---------- Bulk import ----------

    async def import_transactions(self, file: UploadFile, current_user) -> ImportResult:
        return await self.service.import_transactions(file=file, user_id=current_user.id)