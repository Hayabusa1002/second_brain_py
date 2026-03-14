from typing import Optional
from uuid import UUID
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