from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db, require_admin
from app.controllers.subcategory_controller import SubcategoryController
from app.services.subcategory_service import SubcategoryService
from app.repositories.subcategory_repository import SubcategoryRepository
from app.repositories.category_repository import CategoryRepository
from app.schemas.subcategory import (
    SubcategoryCreate,
    SubcategoryUpdate,
    SubcategoryResponse,
)


router = APIRouter(
    prefix="/categories/{category_id}/subcategories",
    tags=["subcategories"],
    dependencies=[Depends(require_admin)],
)


def get_controller(db: Session = Depends(get_db)) -> SubcategoryController:
    sub_repo = SubcategoryRepository(db)
    cat_repo = CategoryRepository(db)
    service = SubcategoryService(sub_repo, cat_repo)
    return SubcategoryController(service)


@router.get("/", response_model=List[SubcategoryResponse])
def list_subcategories(
    category_id: UUID,
    controller: SubcategoryController = Depends(get_controller),
):
    return controller.list_subcategories(category_id)


@router.get("/{subcategory_id}", response_model=SubcategoryResponse)
def get_subcategory(
    category_id: UUID,
    subcategory_id: UUID,
    controller: SubcategoryController = Depends(get_controller),
):
    subcategory = controller.get_subcategory(category_id, subcategory_id)

    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    return subcategory


@router.post("/", response_model=SubcategoryResponse, status_code=201)
def create_subcategory(
    category_id: UUID,
    data: SubcategoryCreate,
    controller: SubcategoryController = Depends(get_controller),
):
    subcategory = controller.create_subcategory(category_id, data)

    if not subcategory:
        raise HTTPException(status_code=400, detail="Invalid category")

    return subcategory


@router.patch("/{subcategory_id}", response_model=SubcategoryResponse)
def update_subcategory(
    category_id: UUID,
    subcategory_id: UUID,
    data: SubcategoryUpdate,
    controller: SubcategoryController = Depends(get_controller),
):
    updated = controller.update_subcategory(category_id, subcategory_id, data)

    if not updated:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    return updated


@router.delete("/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subcategory(
    category_id: UUID,
    subcategory_id: UUID,
    controller: SubcategoryController = Depends(get_controller),
):
    deleted = controller.delete_subcategory(category_id, subcategory_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    return