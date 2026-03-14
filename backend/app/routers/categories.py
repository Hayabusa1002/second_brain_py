from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.controllers.category_controller import CategoryController
from app.services.category_service import CategoryService
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter()

def get_controller(db: Session = Depends(get_db)) -> CategoryController:
    repository = CategoryRepository(db)
    service    = CategoryService(repository)
    return CategoryController(service)

@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(controller: CategoryController = Depends(get_controller)):
    return controller.list_categories()

@router.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CategoryCreate,
    controller: CategoryController = Depends(get_controller)
):
    return controller.create_category(data)