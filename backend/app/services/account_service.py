from typing import Optional
from uuid import UUID
from app.repositories.account_repository import AccountRepository
class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def list_accounts(self, user_id: UUID):
        return self.repository.list(user_id=user_id)

    def get_account(self, account_id: UUID):
        return self.repository.get_by_id(account_id)