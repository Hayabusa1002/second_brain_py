from typing import Optional
from uuid import UUID
from fastapi import UploadFile

from app.services.import_service import ImportService
from app.repositories.category_repository import CategoryRepository
from app.repositories.account_repository import AccountRepository
class TransactionController:
    def __init__(self, service):
        self.service = service

    def create_transaction(self, data):
        return self.service.create_transaction(data)

    def list_transactions(
        self,
        type: Optional[str] = None,
        category_id: Optional[UUID] = None,
        account_id: Optional[UUID] = None,
    ):
        return self.service.list_transactions(type=type, category_id=category_id, account_id=account_id)

    async def import_transactions(self, file: UploadFile):
        content = await file.read()
        import_service = ImportService(
            transaction_repo=self.service.repository,
            category_repo=CategoryRepository(),
            account_repo=AccountRepository(),
        )
        return import_service.import_file(content, file.filename.lower())