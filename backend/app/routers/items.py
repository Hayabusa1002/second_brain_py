from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controllers.item_controller import ItemController
from app.db.deps import get_current_user, get_db
from app.repositories.item_repository import ItemRepository
from app.repositories.subcategory_repository import SubcategoryRepository
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.services.helpers.import_service import BulkImportService
from app.services.imports.item_import import ItemImportService
from app.services.item_service import (
    DuplicateItemError,
    ItemNotFoundError,
    ItemService,
    ItemSubcategoryNotFoundError,
)


router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_current_user)],
)


def get_controller(db: Session = Depends(get_db)) -> ItemController:
    repository = ItemRepository(db)
    subcategory_repository = SubcategoryRepository(db)
    bulk_import_service = BulkImportService()

    import_service = ItemImportService(
        repository=repository,
        subcategory_repository=subcategory_repository,
        bulk_import_service=bulk_import_service,
    )

    service = ItemService(
        repository=repository,
        subcategory_repository=subcategory_repository,
        import_service=import_service,
    )
    return ItemController(service)


# ---------- Reads ----------

@router.get("", response_model=List[ItemResponse])
def list_items(
    controller: ItemController = Depends(get_controller),
):
    return controller.list_items()


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: UUID,
    controller: ItemController = Depends(get_controller),
):
    try:
        return controller.get_item(item_id)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{item_id}/subcategories")
def list_item_subcategories(
    item_id: UUID,
    controller: ItemController = Depends(get_controller),
):
    try:
        return controller.list_item_subcategories(item_id)
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ---------- Writes ----------

@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    data: ItemCreate,
    controller: ItemController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        return controller.create_item(data=data, user_id=user.id)
    except DuplicateItemError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ItemSubcategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: UUID,
    data: ItemUpdate,
    controller: ItemController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        return controller.update_item(
            item_id=item_id,
            data=data,
            user_id=user.id,
        )
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateItemError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ItemSubcategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: UUID,
    controller: ItemController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        controller.delete_item(item_id=item_id, user_id=user.id)
        return
    except ItemNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))