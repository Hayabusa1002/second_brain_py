from app.services.balance_service import BalanceService
from app.repositories.transaction_repository import TransactionRepository

class AccountController:
    def __init__(self):
        self.repository = TransactionRepository()
        self.balance_service = BalanceService()

    def get_balance(self, account_id):
        transactions = self.repository.get_by_account(account_id)
        return self.balance_service.calculate_balance(transactions)