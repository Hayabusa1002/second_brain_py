from typing import List
from uuid import UUID
import json

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import PlainTextResponse, Response
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.controllers.category_controller import CategoryController
from app.services.category_service import CategoryService
from app.repositories.category_repository import CategoryRepository
from app.repositories.subcategory_repository import SubcategoryRepository
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.schemas.bulk_import import ImportResult

router = APIRouter()

TEMPLATE_CSV = """name,type,subcategory_names
Job,income,Salary | Holiday Pay
Freelance,income,Projects | Tips | Bonus
Market,expense,Food | Cleaning
Technology & Devices,expense,Smartphone | Laptop / Computer | Apps / In-App Purchases
"""

TEMPLATE_JSON = [
    {
        "name": "Job",
        "type": "income",
        "subcategories": [
            {"name": "Salary"},
            {"name": "Holiday Pay"},
        ],
    },
    {
        "name": "Freelance",
        "type": "income",
        "subcategories": [
            {"name": "Projects"},
            {"name": "Tips"},
            {"name": "Bonus"},
        ],
    },
    {
        "name": "Market",
        "type": "expense",
        "subcategories": [
            {"name": "Food"},
            {"name": "Cleaning"},
        ],
    },
    {
        "name": "Technology & Devices",
        "type": "expense",
        "subcategories": [
            {"name": "Smartphone"},
            {"name": "Laptop / Computer"},
            {"name": "Apps / In-App Purchases"},
        ],
    },
]

TEMPLATE_YAML = """- name: Job
  type: income
  subcategories:
    - name: Salary
    - name: Holiday Pay

- name: Freelance
  type: income
  subcategories:
    - name: Projects
    - name: Tips
    - name: Bonus

- name: Market
  type: expense
  subcategories:
    - name: Food
    - name: Cleaning

- name: Technology & Devices
  type: expense
  subcategories:
    - name: Smartphone
    - name: Laptop / Computer
    - name: Apps / In-App Purchases
"""


def get_controller(db: Session = Depends(get_db)) -> CategoryController:
    category_repository = CategoryRepository(db)
    subcategory_repository = SubcategoryRepository(db)
    service = CategoryService(category_repository, subcategory_repository)
    return CategoryController(service)


# --------- IMPORT TEMPLATES ---------


@router.get("/categories/import/template/csv", response_class=PlainTextResponse)
def download_categories_template_csv(
    current_user=Depends(get_current_user),
):
    return PlainTextResponse(
        content=TEMPLATE_CSV,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=categories_template.csv",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.get("/categories/import/template/json")
def download_categories_template_json(
    current_user=Depends(get_current_user),
):
    return Response(
        content=json.dumps(TEMPLATE_JSON, indent=2),
        media_type="application/json",
        headers={
            "Content-Disposition": "attachment; filename=categories_template.json",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.get("/categories/import/template/yaml", response_class=PlainTextResponse)
def download_categories_template_yaml(
    current_user=Depends(get_current_user),
):
    return PlainTextResponse(
        content=TEMPLATE_YAML,
        media_type="application/x-yaml",
        headers={
            "Content-Disposition": "attachment; filename=categories_template.yaml",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


# --------- IMPORT ---------


@router.post("/categories/import", response_model=ImportResult)
async def import_categories(
    file: UploadFile = File(...),
    controller: CategoryController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    if not file.filename or not any(
        file.filename.lower().endswith(ext)
        for ext in (".csv", ".xlsx", ".xls", ".json", ".yaml", ".yml")
    ):
        raise HTTPException(
            status_code=400,
            detail="Unsupported format. Use CSV, XLSX, JSON or YAML.",
        )

    try:
        return await controller.import_categories(file, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --------- CRUD ---------


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
    try:
        deleted = controller.delete_category(category_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Category not found")
        return
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))