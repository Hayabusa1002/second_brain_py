from app.services.category_service import CategoryService

class CategoryController:
    
    def __init__(self, service: CategoryService):
        self.service = service

    def list_categories(self):
        return self.service.list_categories()

    def create_category(self, data):
        return self.service.create_category(data)