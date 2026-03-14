from typing import List
from fastapi import APIRouter

from app.controllers.category_controller import CategoryController
from app.services.category_service import CategoryService
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter()

repository = CategoryRepository()
service = CategoryService(repository)
controller = CategoryController(service)

@router.get("/categories", response_model=List[CategoryResponse])
def list_categories():
    return controller.list_categories()

@router.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(data: CategoryCreate):
    return controller.create_category(data)