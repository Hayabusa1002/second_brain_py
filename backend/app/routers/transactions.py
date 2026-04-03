from typing import List, Optional
from uuid import UUID
from datetime import date

from fastapi import APIRouter, Query, UploadFile, File, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.controllers.transaction_controller import TransactionController
from app.services.transaction_service import TransactionService
from app.repositories.transaction_repository import TransactionRepository
from app.models.transaction import TransactionType, PaymentMethod
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionDetailResponse,
)
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.schemas.bulk_import import ImportResult
from app.core.exceptions import NotFoundError


router = APIRouter()


TEMPLATE_CSV = """date,amount,type,payment_method,category,subcategory,account,store,city,paid_by,paid_to,description
2026-01-15,50000,expense,debit,Food,Restaurant,Personal,Crepes & Waffles,Medellin,Luis,Luis,Lunch at restaurant
2026-01-16,2000000,income,transfer,Salary,Monthly Salary,Personal,,,,,Monthly salary
2026-01-17,30000,expense,cash,Transport,Bus,Shared,Metro,Medellin,Luis,Daniel,Bus tickets
2026-01-18,15000,expense,credit,Entertainment,Cinema,Shared,Cine Colombia,Medellin,Daniel,Daniel,Movie night
"""


def get_controller(db: Session = Depends(get_db)) -> TransactionController:
    repository = TransactionRepository(db)
    service = TransactionService(repository)
    return TransactionController(service, db)


@router.get("/transactions/import/template", response_class=PlainTextResponse)
def download_template():
    return PlainTextResponse(
        content=TEMPLATE_CSV,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=import_template.csv"},
    )


@router.post("/transactions/import", response_model=ImportResult)
async def import_transactions(
    file: UploadFile = File(...),
    controller: TransactionController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    if not file.filename or not any(file.filename.lower().endswith(ext) for ext in (".csv", ".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Unsupported format. Use .csv or .xlsx")

    try:
        return await controller.import_transactions(file, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/transactions", response_model=List[TransactionResponse])
def list_transactions(
    type: Optional[TransactionType] = Query(default=None),
    payment_method: Optional[PaymentMethod] = Query(default=None),
    category_id: Optional[UUID] = Query(default=None),
    subcategory_id: Optional[UUID] = Query(default=None),
    account_id: Optional[UUID] = Query(default=None),
    store_id: Optional[UUID] = Query(default=None),
    city_id: Optional[UUID] = Query(default=None),
    paid_by: Optional[UUID] = Query(default=None),
    paid_to: Optional[UUID] = Query(default=None),
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
    q: Optional[str] = Query(default=None),
    controller: TransactionController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    return controller.list_transactions(
        type=type,
        payment_method=payment_method,
        category_id=category_id,
        subcategory_id=subcategory_id,
        account_id=account_id,
        store_id=store_id,
        city_id=city_id,
        paid_by=paid_by,
        paid_to=paid_to,
        date_from=date_from,
        date_to=date_to,
        q=q,
        user_id=current_user.id,
    )


@router.post("/transactions", response_model=TransactionResponse, status_code=201)
def create_transaction(
    data: TransactionCreate,
    controller: TransactionController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    return controller.create_transaction(data, current_user)


@router.get("/transactions/{transaction_id}", response_model=TransactionDetailResponse)
def get_transaction(
    transaction_id: UUID,
    controller: TransactionController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    tx = controller.get_transaction(transaction_id, user_id=current_user.id)
    if tx is None:
        raise NotFoundError("Transaction")
    return tx


@router.patch("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: UUID,
    data: TransactionUpdate,
    controller: TransactionController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    tx = controller.update_transaction(transaction_id, data, user_id=current_user.id)
    if tx is None:
        raise NotFoundError("Transaction")
    return tx


@router.delete("/transactions/{transaction_id}", status_code=204)
def delete_transaction(
    transaction_id: UUID,
    controller: TransactionController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    deleted = controller.delete_transaction(transaction_id, user_id=current_user.id)
    if not deleted:
        raise NotFoundError("Transaction")
    return None


@router.get("/transactions/{transaction_id}/items", response_model=List[ItemResponse])
def list_items(
    transaction_id: UUID,
    controller: TransactionController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    items = controller.list_items(transaction_id, user_id=current_user.id)
    if items is None:
        raise NotFoundError("Transaction")
    return items


@router.post("/transactions/{transaction_id}/items", response_model=ItemResponse, status_code=201)
def create_item(
    transaction_id: UUID,
    data: ItemCreate,
    controller: TransactionController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    item = controller.create_item(transaction_id, data, user_id=current_user.id)
    if item is None:
        raise NotFoundError("Transaction")
    return item


@router.patch("/transactions/{transaction_id}/items/{item_id}", response_model=ItemResponse)
def update_item(
    transaction_id: UUID,
    item_id: UUID,
    data: ItemUpdate,
    controller: TransactionController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    item = controller.update_item(transaction_id, item_id, data, user_id=current_user.id)
    if item is None:
        raise NotFoundError("Item")
    return item


@router.delete("/transactions/{transaction_id}/items/{item_id}", status_code=204)
def delete_item(
    transaction_id: UUID,
    item_id: UUID,
    controller: TransactionController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    deleted = controller.delete_item(transaction_id, item_id, user_id=current_user.id)
    if not deleted:
        raise NotFoundError("Item")
    return None