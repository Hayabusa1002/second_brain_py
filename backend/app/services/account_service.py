from typing import List, Optional
import uuid
from app.repositories.account_repository import AccountRepository, AccountRecord

class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def list_accounts(self) -> List[AccountRecord]:
        return self.repository.list()

    def get_account(self, account_id: uuid.UUID) -> Optional[AccountRecord]:
        return self.repository.get_by_id(account_id)