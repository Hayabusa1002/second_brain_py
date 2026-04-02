from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services.item_service import ItemService


router = APIRouter(
    prefix="/items",
    tags=["items"],
)


def get_service(db: Session = Depends(get_db)) -> ItemService:
    return ItemService(db)


@router.get("/by-transaction/{transaction_id}", response_model=List[ItemResponse])
def list_items_by_transaction(
    transaction_id: UUID,
    service: ItemService = Depends(get_service),
    current_user=Depends(get_current_user),
):
    items = service.list_items(transaction_id, current_user.id)
    if items is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return items


@router.post("/transactions/{transaction_id}", response_model=ItemResponse, status_code=201)
def create_item_for_transaction(
    transaction_id: UUID,
    data: ItemCreate,
    service: ItemService = Depends(get_service),
    current_user=Depends(get_current_user),
):
    item = service.create_item(transaction_id, data, current_user.id)
    if item is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return item


@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: UUID,
    data: ItemUpdate,
    service: ItemService = Depends(get_service),
    current_user=Depends(get_current_user),
):
    # Aquí necesitarías que ItemService resuelva el transaction_id internamente
    # o expongas un método get/update por item_id.
    raise HTTPException(status_code=501, detail="Not implemented")