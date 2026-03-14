from typing import Optional
import uuid
from app.repositories.account_repository import AccountRepository
class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def list_accounts(self):
        return self.repository.list()

    def get_account(self, account_id: uuid.UUID):
        return self.repository.get_by_id(account_id)