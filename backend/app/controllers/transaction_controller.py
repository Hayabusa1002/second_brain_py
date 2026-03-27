from typing import Optional
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.services.import_service import ImportService
from app.repositories.category_repository import CategoryRepository
from app.repositories.account_repository import AccountRepository


class TransactionController:

    def __init__(self, service, db: Session):
        self.service = service
        self.db = db

    def list_transactions(
        self,
        user_id: UUID,
        type: Optional[str] = None,
        category_id: Optional[UUID] = None,
        account_id: Optional[UUID] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        q: Optional[str] = None,
    ):
        return self.service.list_transactions(
            user_id=user_id,
            type=type,
            category_id=category_id,
            account_id=account_id,
            date_from=date_from,
            date_to=date_to,
            q=q,
        )

    async def import_transactions(self, file: UploadFile, current_user):
        content = await file.read()
        import_service = ImportService(
            transaction_repo=self.service.repository,
            category_repo=CategoryRepository(self.db),
            account_repo=AccountRepository(self.db),
        )
        return import_service.import_file(content, file.filename.lower(), current_user.id)

    def create_transaction(self, data, current_user):
        return self.service.create_transaction(data, current_user.id)

    def update_transaction(self, transaction_id: UUID, data, user_id: UUID):
        tx = self.service.get_by_id(transaction_id)
        if not tx:
            return None
        return self.service.update(transaction_id, data)

    def get_transaction(self, transaction_id: UUID, user_id: UUID):
        return self.service.get_by_id(transaction_id)

    def delete_transaction(self, transaction_id: UUID, user_id: UUID) -> bool:
        return self.service.delete(transaction_id)