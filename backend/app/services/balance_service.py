from decimal import Decimal

class BalanceService:
    def calculate_balance(self, transactions):
        balance = Decimal("0")

        for t in transactions:
            if t.type == "income":
                balance += t.amount

            if t.type == "expense":
                balance -= t.amount

        return balance