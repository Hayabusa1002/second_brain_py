import uuid
from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models.account import Account
from app.models.account_owner import account_owners
from app.schemas.account import AccountCreate, AccountUpdate


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    # ---------- Reads ----------

    def list(self, user_id: UUID) -> List[Account]:
        return (
            self.db.query(Account)
            .join(account_owners, account_owners.c.account_id == Account.id)
            .options(selectinload(Account.owners), selectinload(Account.transactions))
            .filter(account_owners.c.user_id == user_id)
            .all()
        )

    def list_owner_ids(self, account_id: UUID) -> List[UUID]:
        rows = self.db.execute(
            account_owners.select().where(
                account_owners.c.account_id == account_id
            )
        ).fetchall()

        return [row.user_id for row in rows]

    def get_by_id(self, account_id: UUID) -> Optional[Account]:
        return (
            self.db.query(Account)
            .options(selectinload(Account.owners), selectinload(Account.transactions))
            .filter(Account.id == account_id)
            .first()
        )

    def get_by_name_for_user(self, name: str, user_id: UUID) -> Optional[Account]:
        normalized_name = name.strip()

        return (
            self.db.query(Account)
            .join(account_owners, account_owners.c.account_id == Account.id)
            .options(selectinload(Account.owners), selectinload(Account.transactions))
            .filter(
                account_owners.c.user_id == user_id,
                Account.name.ilike(normalized_name),
            )
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

    # ---------- Owners assignation ----------

    def assign_owner(self, account_id: UUID, user_id: UUID) -> None:
        self.db.execute(
            account_owners.insert().values(
                account_id=account_id,
                user_id=user_id,
            )
        )
        self.db.commit()

    def unassign_owner(self, account_id: UUID, user_id: UUID) -> None:
        self.db.execute(
            account_owners.delete().where(
                account_owners.c.account_id == account_id,
                account_owners.c.user_id == user_id,
            )
        )
        self.db.commit()