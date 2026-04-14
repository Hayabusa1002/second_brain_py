from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

import json

from app.controllers.store_controller import StoreController
from app.db.deps import get_current_user, get_db
from app.repositories.store_repository import StoreRepository
from app.routers.helpers.downloads import build_template_download
from app.routers.templates.stores import (
    TEMPLATE_CSV,
    TEMPLATE_JSON,
    TEMPLATE_YAML,
)
from app.schemas.bulk_import import ImportResult
from app.schemas.store import (
    StoreCreate,
    StoreResponse,
    StoreSubcategoryAssign,
    StoreUpdate,
)
from app.schemas.subcategory import SubcategoryResponse
from app.services.helpers.import_service import UnsupportedImportFormatError
from app.services.store_service import (
    DuplicateStoreError,
    StoreNotFoundError,
    StoreService,
)


router = APIRouter(prefix="/stores", tags=["stores"])


def get_controller(db: Session = Depends(get_db)) -> StoreController:
    repository = StoreRepository(db)
    service = StoreService(repository)
    return StoreController(service)


# ---------- Import templates ----------

@router.get("/import/template/csv")
def download_stores_template_csv():
    return build_template_download(
        content=TEMPLATE_CSV,
        filename="stores_template.csv",
        media_type="text/csv",
    )


@router.get("/import/template/json")
def download_stores_template_json():
    return build_template_download(
        content=json.dumps(TEMPLATE_JSON, indent=2),
        filename="stores_template.json",
        media_type="application/json",
    )


@router.get("/import/template/yaml")
def download_stores_template_yaml():
    return build_template_download(
        content=TEMPLATE_YAML,
        filename="stores_template.yaml",
        media_type="application/x-yaml",
    )


# ---------- Import ----------

@router.post("/import", response_model=ImportResult)
async def import_stores(
    file: UploadFile = File(...),
    controller: StoreController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        return await controller.import_stores(file=file, current_user=user)
    except UnsupportedImportFormatError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ---------- Reads ----------

@router.get("", response_model=List[StoreResponse])
def list_stores(
    controller: StoreController = Depends(get_controller),
):
    return controller.list_stores()


@router.get("/{store_id}", response_model=StoreResponse)
def get_store(
    store_id: UUID,
    controller: StoreController = Depends(get_controller),
):
    try:
        return controller.get_store(store_id)
    except StoreNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ---------- Writes ----------

@router.post("", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
def create_store(
    data: StoreCreate,
    controller: StoreController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        return controller.create_store(data=data, user_id=user.id)
    except DuplicateStoreError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{store_id}", response_model=StoreResponse)
def update_store(
    store_id: UUID,
    data: StoreUpdate,
    controller: StoreController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        return controller.update_store(store_id=store_id, data=data, user_id=user.id)
    except StoreNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateStoreError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store(
    store_id: UUID,
    controller: StoreController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        controller.delete_store(store_id=store_id, user_id=user.id)
        return
    except StoreNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ---------- Store subcategories ----------

@router.get("/{store_id}/subcategories", response_model=List[SubcategoryResponse])
def list_store_subcategories(
    store_id: UUID,
    controller: StoreController = Depends(get_controller),
):
    try:
        return controller.list_store_subcategories(store_id)
    except StoreNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put(
    "/{store_id}/subcategories",
    response_model=List[SubcategoryResponse],
)
def replace_store_subcategories(
    store_id: UUID,
    data: StoreSubcategoryAssign,
    controller: StoreController = Depends(get_controller),
):
    try:
        return controller.replace_store_subcategories(store_id=store_id, subcategory_ids=data.subcategory_ids)
    except StoreNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))