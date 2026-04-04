from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.controllers.category_controller import CategoryController
from app.services.category_service import CategoryService
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)


router = APIRouter()


def get_controller(db: Session = Depends(get_db)) -> CategoryController:
    repository = CategoryRepository(db)
    service = CategoryService(repository)
    return CategoryController(service)


@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(
    controller: CategoryController = Depends(get_controller),
):
    return controller.list_categories()


@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: UUID,
    controller: CategoryController = Depends(get_controller),
):
    category = controller.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CategoryCreate,
    controller: CategoryController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    return controller.create_category(data)


@router.patch("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    controller: CategoryController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    category = controller.update_category(category_id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: UUID,
    controller: CategoryController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    deleted = controller.delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return