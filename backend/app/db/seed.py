import uuid
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.models.category import Category, CategoryType
from app.models.account import Account, AccountType
from app.core.security import hash_password

DEFAULT_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000099")

DEFAULT_CATEGORIES = [
    {"id": uuid.UUID("10000000-0000-0000-0000-000000000001"), "name": "Salary",        "type": CategoryType.income},
    {"id": uuid.UUID("10000000-0000-0000-0000-000000000002"), "name": "Freelance",     "type": CategoryType.income},
    {"id": uuid.UUID("10000000-0000-0000-0000-000000000003"), "name": "Other income",  "type": CategoryType.income},
    {"id": uuid.UUID("20000000-0000-0000-0000-000000000001"), "name": "Food",          "type": CategoryType.expense},
    {"id": uuid.UUID("20000000-0000-0000-0000-000000000002"), "name": "Transport",     "type": CategoryType.expense},
    {"id": uuid.UUID("20000000-0000-0000-0000-000000000003"), "name": "Housing",       "type": CategoryType.expense},
    {"id": uuid.UUID("20000000-0000-0000-0000-000000000004"), "name": "Entertainment", "type": CategoryType.expense},
    {"id": uuid.UUID("20000000-0000-0000-0000-000000000005"), "name": "Health",        "type": CategoryType.expense},
    {"id": uuid.UUID("20000000-0000-0000-0000-000000000006"), "name": "Other expense", "type": CategoryType.expense},
]

DEFAULT_ACCOUNTS = [
    {"id": uuid.UUID("00000000-0000-0000-0000-000000000001"), "name": "Personal", "type": AccountType.individual},
    {"id": uuid.UUID("00000000-0000-0000-0000-000000000002"), "name": "Shared",   "type": AccountType.shared},
]


def seed(db: Session) -> None:

    if not db.query(User).filter(User.id == DEFAULT_USER_ID).first():
        db.add(User(
            id=DEFAULT_USER_ID,
            name="Default User",
            email="default@secondbrain.app",
            password=hash_password("placeholder"),
            role=UserRole.owner
        ))

    if not db.query(Category).first():
        for data in DEFAULT_CATEGORIES:
            db.add(Category(**data))

    if not db.query(Account).first():
        for data in DEFAULT_ACCOUNTS:
            db.add(Account(**data))

    db.commit()