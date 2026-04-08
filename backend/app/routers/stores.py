from typing import List
from uuid import UUID
import json

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import PlainTextResponse, Response
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.controllers.store_controller import StoreController
from app.services.store_service import StoreService
from app.repositories.store_repository import StoreRepository
from app.schemas.store import (
    StoreCreate,
    StoreUpdate,
    StoreResponse,
    StoreSubcategoryAssign,
    StoreSubcategoryLinkResponse,
)
from app.schemas.bulk_import import ImportResult


router = APIRouter()


TEMPLATE_CSV = """name,type,address,website,subcategory_names
Exito,physical,Carrera 43A # 1 Sur-150,,Food|Groceries|Household
Carulla,physical,Calle 10 # 43E-135,,Food|Groceries
Spotify,subscription,,https://spotify.com,Music|Entertainment
Netflix,subscription,,https://netflix.com,Streaming|Entertainment
Steam,online,,https://store.steampowered.com,Games|Digital Products
"""


TEMPLATE_JSON = [
    {
        "name": "Exito",
        "type": "physical",
        "address": "Carrera 43A # 1 Sur-150",
        "website": None,
        "subcategories": ["Food", "Groceries", "Household"],
    },
    {
        "name": "Carulla",
        "type": "physical",
        "address": "Calle 10 # 43E-135",
        "website": None,
        "subcategories": ["Food", "Groceries"],
    },
    {
        "name": "Spotify",
        "type": "subscription",
        "address": None,
        "website": "https://spotify.com",
        "subcategories": ["Music", "Entertainment"],
    },
    {
        "name": "Netflix",
        "type": "subscription",
        "address": None,
        "website": "https://netflix.com",
        "subcategories": ["Streaming", "Entertainment"],
    },
    {
        "name": "Steam",
        "type": "online",
        "address": None,
        "website": "https://store.steampowered.com",
        "subcategories": ["Games", "Digital Products"],
    },
]


TEMPLATE_YAML = """- name: Exito
  type: physical
  address: Carrera 43A # 1 Sur-150
  website:
  subcategories:
    - Food
    - Groceries
    - Household

- name: Carulla
  type: physical
  address: Calle 10 # 43E-135
  website:
  subcategories:
    - Food
    - Groceries

- name: Spotify
  type: subscription
  address:
  website: https://spotify.com
  subcategories:
    - Music
    - Entertainment

- name: Netflix
  type: subscription
  address:
  website: https://netflix.com
  subcategories:
    - Streaming
    - Entertainment

- name: Steam
  type: online
  address:
  website: https://store.steampowered.com
  subcategories:
    - Games
    - Digital Products
"""


def get_controller(db: Session = Depends(get_db)) -> StoreController:
    repository = StoreRepository(db)
    service = StoreService(repository)
    return StoreController(service)


# --------- IMPORT TEMPLATES ---------


@router.get("/stores/import/template/csv", response_class=PlainTextResponse)
def download_stores_template_csv(
    current_user=Depends(get_current_user),
):
    return PlainTextResponse(
        content=TEMPLATE_CSV,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=stores_template.csv",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.get("/stores/import/template/json")
def download_stores_template_json(
    current_user=Depends(get_current_user),
):
    return Response(
        content=json.dumps(TEMPLATE_JSON, indent=2),
        media_type="application/json",
        headers={
            "Content-Disposition": "attachment; filename=stores_template.json",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.get("/stores/import/template/yaml", response_class=PlainTextResponse)
def download_stores_template_yaml(
    current_user=Depends(get_current_user),
):
    return PlainTextResponse(
        content=TEMPLATE_YAML,
        media_type="application/x-yaml",
        headers={
            "Content-Disposition": "attachment; filename=stores_template.yaml",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


# --------- IMPORT ---------


@router.post("/stores/import", response_model=ImportResult)
async def import_stores(
    file: UploadFile = File(...),
    controller: StoreController = Depends(get_controller),
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
        return await controller.import_stores(file, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --------- CRUD ---------


@router.get("/stores", response_model=List[StoreResponse])
def list_stores(
    controller: StoreController = Depends(get_controller),
):
    return controller.list_stores()


@router.get("/stores/{store_id}", response_model=StoreResponse)
def get_store(
    store_id: UUID,
    controller: StoreController = Depends(get_controller),
):
    store = controller.get_store(store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.post("/stores", response_model=StoreResponse, status_code=201)
def create_store(
    data: StoreCreate,
    controller: StoreController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    return controller.create_store(data)


@router.patch("/stores/{store_id}", response_model=StoreResponse)
def update_store(
    store_id: UUID,
    data: StoreUpdate,
    controller: StoreController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    store = controller.update_store(store_id, data)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.delete("/stores/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store(
    store_id: UUID,
    controller: StoreController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    deleted = controller.delete_store(store_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Store not found")
    return


# --------- STORE SUBCATEGORIES ---------


@router.get(
    "/stores/{store_id}/subcategories",
    response_model=List[StoreSubcategoryLinkResponse],
)
def list_store_subcategories(
    store_id: UUID,
    controller: StoreController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    try:
        return controller.list_store_subcategories(store_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/stores/{store_id}/subcategories",
    response_model=List[StoreSubcategoryLinkResponse],
)
def replace_store_subcategories(
    store_id: UUID,
    data: StoreSubcategoryAssign,
    controller: StoreController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    try:
        return controller.replace_store_subcategories(store_id, data.subcategory_ids)
    except ValueError as e:
        message = str(e)
        if message == "Store not found":
            raise HTTPException(status_code=404, detail=message)
        raise HTTPException(status_code=400, detail=message)