from uuid import UUID

from app.schemas.account import AccountCreate, AccountUpdate
from app.services.account_service import AccountService
from app.services.helpers.balance_service import BalanceService


class AccountController:
    def __init__(
        self,
        service: AccountService,
        balance_service: BalanceService,
    ):
        self.service = service
        self.balance_service = balance_service

    # ---------- Reads ----------

    def list_accounts(self, user_id: UUID):
        return self.service.list_accounts(user_id=user_id)

    def get_account(self, account_id: UUID):
        return self.service.get_account(account_id)

    def get_balance(self, account_id: UUID):
        account = self.get_account(account_id)
        balance = self.balance_service.get_account_balance(account_id)
        return {"account_id": str(account.id), "balance": balance}

    # ---------- Writes ----------

    def create_account(self, data: AccountCreate, user_id: UUID):
        return self.service.create_account(data=data, user_id=user_id)

    def update_account(self, account_id: UUID, data: AccountUpdate, user_id: UUID):
        return self.service.update_account(account_id=account_id, data=data, user_id=user_id)

    def delete_account(self, account_id: UUID) -> bool:
        return self.service.delete_account(account_id)

    # ---------- Owners assignation ----------

    def assign_owner(self, account_id: UUID, user_id: UUID) -> None:
        self.service.assign_owner(account_id=account_id, user_id=user_id)

    def unassign_owner(self, account_id: UUID, user_id: UUID) -> None:
        self.service.unassign_owner(account_id=account_id, user_id=user_id)