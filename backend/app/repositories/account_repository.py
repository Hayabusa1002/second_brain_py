import uuid
from datetime import datetime, UTC
from dataclasses import dataclass, field
from typing import List, Optional
from app.models.account import AccountType

# UUIDs that match with default values in schemas/transaction.py
_INDIVIDUAL_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")
_SHARED_ID     = uuid.UUID("00000000-0000-0000-0000-000000000002")

@dataclass
class AccountRecord:
    id: uuid.UUID
    name: str
    type: AccountType
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

accounts_db: List[AccountRecord] = [
    AccountRecord(id=_INDIVIDUAL_ID, name="Personal",  type=AccountType.individual),
    AccountRecord(id=_SHARED_ID,     name="Shared",    type=AccountType.shared),
]

class AccountRepository:
    def list(self) -> List[AccountRecord]:
        return accounts_db

    def get_by_id(self, account_id: uuid.UUID) -> Optional[AccountRecord]:
        return next((a for a in accounts_db if a.id == account_id), None)