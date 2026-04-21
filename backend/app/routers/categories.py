import json
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.controllers.category_controller import CategoryController
from app.db.deps import get_current_user, get_db
from app.repositories.category_repository import CategoryRepository
from app.repositories.subcategory_repository import SubcategoryRepository
from app.routers.helpers.downloads import build_template_download
from app.routers.templates.categories import (
    TEMPLATE_CSV,
    TEMPLATE_JSON,
    TEMPLATE_YAML,
)
from app.schemas.bulk_import import ImportResult
from app.services.helpers.import_service import UnsupportedImportFormatError
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import (
    CategoryNotFoundError,
    CategoryService,
    DuplicateCategoryError,
)


router = APIRouter(
    prefix="/categories",
    dependencies=[Depends(get_current_user)],
)


def get_controller(db: Session = Depends(get_db)) -> CategoryController:
    category_repository = CategoryRepository(db)
    subcategory_repository = SubcategoryRepository(db)
    service = CategoryService(category_repository, subcategory_repository)
    return CategoryController(service)


# ---------- Import templates ----------

@router.get("/import/template/csv")
def download_categories_template_csv():
    return build_template_download(
        content=TEMPLATE_CSV,
        filename="categories_template.csv",
        media_type="text/csv",
    )


@router.get("/import/template/json")
def download_categories_template_json():
    return build_template_download(
        content=json.dumps(TEMPLATE_JSON, indent=2),
        filename="categories_template.json",
        media_type="application/json",
    )


@router.get("/import/template/yaml")
def download_categories_template_yaml():
    return build_template_download(
        content=TEMPLATE_YAML,
        filename="categories_template.yaml",
        media_type="application/x-yaml",
    )


# ---------- Import ----------

@router.post("/import", response_model=ImportResult)
async def import_categories(
    file: UploadFile = File(...),
    controller: CategoryController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    try:
        return await controller.import_categories(file=file, current_user=current_user)
    except UnsupportedImportFormatError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ---------- Reads ----------

@router.get("", response_model=List[CategoryResponse])
def list_categories(
    controller: CategoryController = Depends(get_controller),
):
    return controller.list_categories()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: UUID,
    controller: CategoryController = Depends(get_controller),
):
    try:
        return controller.get_category(category_id)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ---------- Writes ----------

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    controller: CategoryController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        return controller.create_category(data=data, user_id=user.id)
    except DuplicateCategoryError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    controller: CategoryController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        return controller.update_category(category_id=category_id, data=data, user_id=user.id)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateCategoryError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: UUID,
    controller: CategoryController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        controller.delete_category(category_id=category_id, user_id=user.id)
        return
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))