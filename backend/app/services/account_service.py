from uuid import UUID

from app.models.account import AccountType
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountCreate, AccountUpdate


class AccountNotFoundError(Exception):
    def __init__(self, message: str = "Account not found"):
        super().__init__(message)


class DuplicateAccountNameError(Exception):
    def __init__(self, name: str):
        super().__init__(f"Account '{name}' already exists")


class IndividualAccountOwnerLimitError(Exception):
    def __init__(self, message: str = "Individual accounts can only have one owner"):
        super().__init__(message)


class IndividualAccountOwnerModificationError(Exception):
    def __init__(self, message: str = "Individual account owners cannot be modified"):
        super().__init__(message)


class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    # ---------- Reads ----------

    def list_accounts(self, user_id: UUID):
        return self.repository.list(user_id=user_id)

    def get_account(self, account_id: UUID):
        account = self.repository.get_by_id(account_id)
        if not account:
            raise AccountNotFoundError()
        return account
    
    def get_account_by_name(self, account_name: str):
        existing = self.repository.get_by_name(account_name)
        if existing:
            raise DuplicateAccountNameError(account_name)
        return existing
    
    # ---------- Writes ----------

    def create_account(self, data: AccountCreate, user_id: UUID):
        self.get_account_by_name(data.name)
        return self.repository.create(data=data, user_id=user_id)

    def update_account(self, account_id: UUID, data: AccountUpdate, user_id: UUID):
        self.get_account(account_id)
        if data.name is not None:
            self.get_account_by_name(data.name)
        return self.repository.update(account_id=account_id, data=data, user_id=user_id)

    def delete_account(self, account_id: UUID) -> bool:
        self.get_account(account_id)
        return self.repository.delete(account_id)

    # ---------- Owners assignation ----------

    def assign_owner(self, account_id: UUID, user_id: UUID) -> None:
        account = self.get_account(account_id)
        existing_owners = self.repository.list_owner_ids(account_id)

        if account.type == AccountType.individual and existing_owners and user_id not in existing_owners:
            raise IndividualAccountOwnerLimitError()

        if user_id in existing_owners:
            return

        self.repository.assign_owner(account_id, user_id)

    def unassign_owner(self, account_id: UUID, user_id: UUID) -> None:
        account = self.get_account(account_id)
        if account.type == AccountType.individual:
            raise IndividualAccountOwnerModificationError()
        self.repository.unassign_owner(account_id, user_id)