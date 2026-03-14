from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.account import Account

class AccountRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[Account]:
        return self.db.query(Account).all()

    def get_by_id(self, account_id: UUID) -> Optional[Account]:
        return self.db.query(Account).filter(Account.id == account_id).first()

    def get_by_name(self, name: str) -> Optional[Account]:
        return self.db.query(Account).filter(Account.name.ilike(name.strip())).first()