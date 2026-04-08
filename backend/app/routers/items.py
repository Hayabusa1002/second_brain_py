from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.controllers.item_controller import ItemController
from app.repositories.item_repository import ItemRepository
from app.repositories.subcategory_repository import SubcategoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.services.item_service import ItemService


router = APIRouter(
    prefix="/items",
    tags=["items"],
)


def get_controller(db: Session = Depends(get_db)) -> ItemController:
    item_repository = ItemRepository(db)
    transaction_repository = TransactionRepository(db)
    subcategory_repository = SubcategoryRepository(db)
    service = ItemService(
        item_repository,
        transaction_repository,
        subcategory_repository,
    )
    return ItemController(service)


@router.get("/by-transaction/{transaction_id}", response_model=List[ItemResponse])
def list_items_by_transaction(
    transaction_id: UUID,
    controller: ItemController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    items = controller.list_items(transaction_id, current_user.id)
    if items is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return items


@router.post("/transactions/{transaction_id}", response_model=ItemResponse, status_code=201)
def create_item_for_transaction(
    transaction_id: UUID,
    data: ItemCreate,
    controller: ItemController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    try:
        item = controller.create_item(transaction_id, data, current_user.id)
        if item is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/transactions/{transaction_id}/{item_id}", response_model=ItemResponse)
def update_item(
    transaction_id: UUID,
    item_id: UUID,
    data: ItemUpdate,
    controller: ItemController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    try:
        item = controller.update_item(transaction_id, item_id, data, current_user.id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/transactions/{transaction_id}/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    transaction_id: UUID,
    item_id: UUID,
    controller: ItemController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    deleted = controller.delete_item(transaction_id, item_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return