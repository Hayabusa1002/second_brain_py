from app.repositories.category_repository import CategoryRepository
class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def list_categories(self):
        return self.repository.list()

    def create_category(self, data):
        return self.repository.add(data)