import uuid
from typing import List
from app.repositories.category_repository import CategoryRepository, CategoryRecord

class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def list_categories(self) -> List[CategoryRecord]:
        return self.repository.list()

    def create_category(self, data) -> CategoryRecord:
        category = CategoryRecord(
            id=uuid.uuid4(),
            name=data.name,
            type=data.type,
        )
        return self.repository.add(category)