import uuid
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.account import Account, AccountType

class AccountRepository:

    def __init__(self, db: Session):
        self.db = db

    def list(self, user_id: UUID) -> List[Account]:
        return self.db.query(Account).filter(Account.created_by == user_id).all()

    def get_by_id(self, account_id: UUID) -> Optional[Account]:
        return self.db.query(Account).filter(Account.id == account_id).first()

    def get_by_name(self, name: str) -> Optional[Account]:
        return self.db.query(Account).filter(Account.name.ilike(name.strip())).first()

    def create(self, name: str, type: AccountType, created_by: UUID) -> Account:
        account = Account(
            id=uuid.uuid4(),
            name=name,
            type=type,
            created_by=created_by,
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update(self, account_id: UUID, name: str | None, type: AccountType | None) -> Optional[Account]:
        account = self.get_by_id(account_id)
        if not account:
            return None
        if name is not None:
            account.name = name
        if type is not None:
            account.type = type
        self.db.commit()
        self.db.refresh(account)
        return account

    def delete(self, account_id: UUID) -> bool:
        account = self.get_by_id(account_id)
        if not account:
            return False
        self.db.delete(account)
        self.db.commit()
        return True