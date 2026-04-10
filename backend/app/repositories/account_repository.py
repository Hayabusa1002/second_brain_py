import uuid
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models.account import Account, AccountType
from app.models.account_owner import account_owners
from app.schemas.account import AccountCreate, AccountUpdate


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Reads ----------

    def list(self, user_id: UUID) -> list[Account]:
        return (
            self.db.query(Account)
            .options(selectinload(Account.owners))
            .filter(Account.created_by == user_id)
            .all()
        )

    def get_by_id(self, account_id: UUID) -> Optional[Account]:
        return (
            self.db.query(Account)
            .options(selectinload(Account.owners))
            .filter(Account.id == account_id)
            .first()
        )

    def get_by_name(self, name: str) -> Optional[Account]:
        return (
            self.db.query(Account)
            .options(selectinload(Account.owners))
            .filter(Account.name.ilike(name.strip()))
            .first()
        )

    # ---------- Writes ----------

    def create(self, data: AccountCreate, user_id: UUID) -> Account:
        account = Account(
            id=uuid.uuid4(),
            name=data.name.strip(),
            type=data.type,
            created_by=user_id,
            updated_by=user_id,
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return self.get_by_id(account.id)

    def update(self, account_id: UUID, data: AccountUpdate, user_id: UUID) -> Optional[Account]:
        account = self.get_by_id(account_id)
        if not account:
            return None
        
        # exclude_unset avoids update as None the non-sended fields
        for field, value in data.model_dump(exclude_unset=True).items():
            if isinstance(value, str):
                value = value.strip()
            setattr(account, field, value)

        account.updated_by = user_id

        self.db.commit()
        self.db.refresh(account)
        return self.get_by_id(account.id)

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

        existing_owners = self.db.execute(
            account_owners.select().where(
                account_owners.c.account_id == account_id
            )
        ).fetchall()

        # Individual accounts can only have one owner
        if account.type == AccountType.individual and existing_owners:
            raise ValueError("Individual accounts can only have one owner")

        already_assigned = any(str(row.user_id) == str(user_id) for row in existing_owners)
        if not already_assigned:
            self.db.execute(
                account_owners.insert().values(
                    account_id=account_id,
                    user_id=user_id,
                )
            )
            self.db.commit()

    def unassign_owner(self, account_id: UUID, user_id: UUID) -> None:
        account = self.get_by_id(account_id)
        if not account:
            raise ValueError("Account not found")

        if account.type == AccountType.individual:
            raise ValueError("Individual account owners cannot be modified")

        self.db.execute(
            account_owners.delete().where(
                account_owners.c.account_id == account_id,
                account_owners.c.user_id == user_id,
            )
        )
        self.db.commit()