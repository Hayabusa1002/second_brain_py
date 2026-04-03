from typing import Optional
from uuid import UUID

from app.models.account import AccountType
from app.repositories.account_repository import AccountRepository


class AccountService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def list_accounts(self, user_id: UUID):
        return self.repository.list(user_id=user_id)

    def get_account(self, account_id: UUID):
        return self.repository.get_by_id(account_id)

    def create_account(self, name: str, type: AccountType, created_by: UUID):
        existing = self.repository.get_by_name(name)
        if existing:
            return existing

        return self.repository.create(
            name=name,
            type=type,
            created_by=created_by,
        )

    def update_account(
        self,
        account_id: UUID,
        name: Optional[str] = None,
        type: Optional[AccountType] = None,
    ):
        account = self.repository.get_by_id(account_id)
        if not account:
            return None

        if name is not None:
            existing = self.repository.get_by_name(name)
            if existing and existing.id != account_id:
                return None

        return self.repository.update(
            account_id=account_id,
            name=name,
            type=type,
        )

    def delete_account(self, account_id: UUID) -> bool:
        return self.repository.delete(account_id)

    def assign_owner(self, account_id: UUID, user_id: UUID) -> None:
        self.repository.assign_owner(account_id, user_id)

    def unassign_owner(self, account_id: UUID, user_id: UUID) -> None:
        self.repository.unassign_owner(account_id, user_id)