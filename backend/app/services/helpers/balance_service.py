from decimal import Decimal

from app.models.transaction import TransactionType


class BalanceService:
    def calculate_balance(self, transactions):
        balance = Decimal("0")

        for t in transactions:
            t_type = t.type.value if isinstance(t.type, TransactionType) else t.type

            if t_type == "income":
                balance += t.amount
            elif t_type == "expense":
                balance -= t.amount

        return balance