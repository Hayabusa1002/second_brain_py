from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.category import Category
class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[Category]:
        return self.db.query(Category).all()

    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_by_name(self, name: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.name.ilike(name.strip())).first()

    def add(self, data) -> Category:
        category = Category(name=data.name, type=data.type)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category