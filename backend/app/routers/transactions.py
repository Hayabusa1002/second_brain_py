from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.controllers.transaction_controller import TransactionController
from app.db.deps import get_current_user, get_db
from app.repositories.transaction_repository import TransactionRepository
from app.routers.helpers.downloads import build_template_download
from app.routers.templates.transactions import TEMPLATE_CSV
from app.schemas.bulk_import import ImportResult
from app.schemas.transaction import (
    TransactionCreate,
    TransactionDetailResponse,
    TransactionListResponse,
    TransactionResponse,
    TransactionUpdate,
)
from app.services.helpers.import_service import UnsupportedImportFormatError
from app.services.transaction_service import (
    TransactionNotFoundError,
    TransactionService,
)


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    dependencies=[Depends(get_current_user)],
)


def get_controller(db: Session = Depends(get_db)) -> TransactionController:
    repository = TransactionRepository(db)
    service = TransactionService(repository)
    return TransactionController(service)


# ---------- Import templates ----------

@router.get("/import/template")
def download_template():
    return build_template_download(
        content=TEMPLATE_CSV,
        filename="transactions_template.csv",
        media_type="text/csv",
    )


# ---------- Import ----------

@router.post("/import", response_model=ImportResult)
async def import_transactions(
    file: UploadFile = File(...),
    controller: TransactionController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        return await controller.import_transactions(file=file, current_user=user)
    except UnsupportedImportFormatError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ---------- Reads ----------

@router.get("", response_model=TransactionListResponse)
def list_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    account_id: Optional[UUID] = Query(default=None),
    controller: TransactionController = Depends(get_controller),
):
    items, total = controller.list_transactions(
        page=page,
        page_size=page_size,
        account_id=account_id,
    )
    return TransactionListResponse(
        items=items,
        total=total,
        page=page,
        limit=page_size,
    )


@router.get("/{transaction_id}", response_model=TransactionDetailResponse)
def get_transaction(
    transaction_id: UUID,
    controller: TransactionController = Depends(get_controller),
):
    try:
        return controller.get_transaction(transaction_id)
    except TransactionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ---------- Writes ----------

@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    data: TransactionCreate,
    controller: TransactionController = Depends(get_controller),
    user=Depends(get_current_user),
):
    return controller.create_transaction(data=data, user_id=user.id)


@router.patch("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: UUID,
    data: TransactionUpdate,
    controller: TransactionController = Depends(get_controller),
    user=Depends(get_current_user),
):
    try:
        return controller.update_transaction(transaction_id=transaction_id, data=data, user_id=user.id)
    except TransactionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: UUID,
    controller: TransactionController = Depends(get_controller),
):
    try:
        return controller.delete_transaction(transaction_id)
    except TransactionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))