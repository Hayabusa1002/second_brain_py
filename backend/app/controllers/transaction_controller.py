from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.services.import_service import ImportService
from app.repositories.category_repository import CategoryRepository
from app.repositories.account_repository import AccountRepository

class TransactionController:

    def __init__(self, service, db: Session):
        self.service = service
        self.db = db

    def create_transaction(self, data):
        return self.service.create_transaction(data)

    def list_transactions(
        self,
        type: Optional[str] = None,
        category_id: Optional[UUID] = None,
        account_id: Optional[UUID] = None
    ):
        return self.service.list_transactions(type=type, category_id=category_id, account_id=account_id)

    async def import_transactions(self, file: UploadFile):
        content = await file.read()
        import_service = ImportService(
            transaction_repo=self.service.repository,
            category_repo=CategoryRepository(self.db),
            account_repo=AccountRepository(self.db)
        )
        return import_service.import_file(content, file.filename.lower())