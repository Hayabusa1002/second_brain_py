from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.controllers.category_controller import CategoryController
from app.services.category_service import CategoryService
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryResponse
from app.core.exceptions import NotFoundError


router = APIRouter()


def get_controller(db: Session = Depends(get_db)) -> CategoryController:
    repository = CategoryRepository(db)
    service    = CategoryService(repository)
    return CategoryController(service)


@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(
    controller: CategoryController = Depends(get_controller)
):
    tx = controller.list_categories()
    if tx is None:
        raise NotFoundError("Category")
    return tx


@router.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CategoryCreate,
    controller: CategoryController = Depends(get_controller),
    current_user=Depends(get_current_user)
):
    return controller.create_category(data)