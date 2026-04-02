from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db, require_admin
from app.controllers.store_controller import StoreController
from app.services.store_service import StoreService
from app.repositories.store_repository import StoreRepository
from app.schemas.store import StoreCreate, StoreUpdate, StoreResponse


router = APIRouter(
    prefix="/stores",
    tags=["stores"],
    dependencies=[Depends(require_admin)],
)


def get_controller(db: Session = Depends(get_db)) -> StoreController:
    repository = StoreRepository(db)
    service = StoreService(repository)
    return StoreController(service)


@router.get("/", response_model=List[StoreResponse])
def list_stores(
    controller: StoreController = Depends(get_controller),
):
    return controller.list_stores()


@router.get("/{store_id}", response_model=StoreResponse)
def get_store(
    store_id: UUID,
    controller: StoreController = Depends(get_controller),
):
    store = controller.get_store(store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.post("/", response_model=StoreResponse, status_code=201)
def create_store(
    data: StoreCreate,
    controller: StoreController = Depends(get_controller),
):
    return controller.create_store(data)


@router.patch("/{store_id}", response_model=StoreResponse)
def update_store(
    store_id: UUID,
    data: StoreUpdate,
    controller: StoreController = Depends(get_controller),
):
    store = controller.update_store(store_id, data)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store