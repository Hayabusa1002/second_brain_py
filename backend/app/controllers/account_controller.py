from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.account_service import AccountService
from app.services.balance_service import BalanceService
from app.repositories.transaction_repository import TransactionRepository

class AccountController:
    
    def __init__(self, service: AccountService, db: Session):
        self.service = service
        self.db = db
        self.balance_service = BalanceService()

    def list_accounts(self, user_id: UUID):
        return self.service.list_accounts(user_id=user_id)

    def get_balance(self, account_id: UUID):
        account = self.service.get_account(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        transactions = TransactionRepository(self.db).get_by_account(account_id)
        balance = self.balance_service.calculate_balance(transactions)
        return {"account_id": str(account_id), "balance": balance}