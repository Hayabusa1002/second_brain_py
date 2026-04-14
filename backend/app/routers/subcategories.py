from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controllers.subcategory_controller import SubcategoryController
from app.db.deps import get_db, require_admin
from app.repositories.category_repository import CategoryRepository
from app.repositories.subcategory_repository import SubcategoryRepository
from app.schemas.subcategory import (
    SubcategoryCreate,
    SubcategoryResponse,
    SubcategoryUpdate,
)
from app.services.subcategory_service import (
    CategoryNotFoundError,
    DuplicateSubcategoryError,
    SubcategoryNotFoundError,
    SubcategoryService,
)


router = APIRouter(
    prefix="/categories/{category_id}/subcategories",
    tags=["subcategories"],
    dependencies=[Depends(require_admin)],
)

base_router = APIRouter(
    prefix="/subcategories",
    tags=["subcategories"],
    dependencies=[Depends(require_admin)],
)


def get_controller(db: Session = Depends(get_db)) -> SubcategoryController:
    sub_repo = SubcategoryRepository(db)
    cat_repo = CategoryRepository(db)
    service = SubcategoryService(sub_repo, cat_repo)
    return SubcategoryController(service)


# ---------- Reads ----------

@base_router.get("", response_model=List[SubcategoryResponse])
def list_all_subcategories(
    controller: SubcategoryController = Depends(get_controller),
):
    return controller.list_subcategories()


@router.get("", response_model=List[SubcategoryResponse])
def list_subcategories(
    category_id: UUID,
    controller: SubcategoryController = Depends(get_controller),
):
    try:
        return controller.list_subcategories_by_category(category_id=category_id)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{subcategory_id}", response_model=SubcategoryResponse)
def get_subcategory(
    category_id: UUID,
    subcategory_id: UUID,
    controller: SubcategoryController = Depends(get_controller),
):
    try:
        return controller.get_subcategory_by_category(
            category_id=category_id,
            subcategory_id=subcategory_id,
        )
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SubcategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ---------- Writes ----------

@router.post("", response_model=SubcategoryResponse, status_code=status.HTTP_201_CREATED)
def create_subcategory(
    category_id: UUID,
    data: SubcategoryCreate,
    controller: SubcategoryController = Depends(get_controller),
    user=Depends(require_admin),
):
    try:
        return controller.create_subcategory(category_id=category_id, data=data, user_id=user.id)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateSubcategoryError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{subcategory_id}", response_model=SubcategoryResponse)
def update_subcategory(
    category_id: UUID,
    subcategory_id: UUID,
    data: SubcategoryUpdate,
    controller: SubcategoryController = Depends(get_controller),
    user=Depends(require_admin),
):
    try:
        return controller.update_subcategory(
            category_id=category_id,
            subcategory_id=subcategory_id,
            data=data,
            user_id=user.id,
        )
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SubcategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateSubcategoryError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subcategory(
    category_id: UUID,
    subcategory_id: UUID,
    controller: SubcategoryController = Depends(get_controller),
):
    try:
        return controller.delete_subcategory(category_id=category_id, subcategory_id=subcategory_id)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SubcategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))