import uuid
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from app.models.account import Account, AccountType
from app.models.account_owner import account_owners


class AccountRepository:

    def __init__(self, db: Session):
        self.db = db

    def list(self, user_id: UUID) -> List[Account]:
        return (
            self.db.query(Account)
            .options(joinedload(Account.owners))
            .filter(Account.created_by == user_id)
            .all()
        )

    def get_by_id(self, account_id: UUID) -> Optional[Account]:
        return (
            self.db.query(Account)
            .options(joinedload(Account.owners))
            .filter(Account.id == account_id)
            .first()
        )

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

    def assign_owner(self, account_id: UUID, user_id: UUID) -> None:
        account = self.get_by_id(account_id)
        if not account:
            raise ValueError("Account not found")
        if account.type == AccountType.individual:
            raise ValueError("No se pueden añadir owners adicionales a una cuenta individual")

        exists = self.db.execute(
            account_owners.select().where(
                account_owners.c.account_id == account_id,
                account_owners.c.user_id == user_id,
            )
        ).first()
        if not exists:
            self.db.execute(
                account_owners.insert().values(account_id=account_id, user_id=user_id)
            )
            self.db.commit()


    def unassign_owner(self, account_id: UUID, user_id: UUID) -> None:
        account = self.get_by_id(account_id)
        if not account:
            raise ValueError("Account not found")
        if account.type == AccountType.individual:
            raise ValueError("No se pueden modificar owners de una cuenta individual")

        self.db.execute(
            account_owners.delete().where(
                account_owners.c.account_id == account_id,
                account_owners.c.user_id == user_id,
            )
        )
        self.db.commit()