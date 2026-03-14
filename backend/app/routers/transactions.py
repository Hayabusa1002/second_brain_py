from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Query, UploadFile, File, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.controllers.transaction_controller import TransactionController
from app.services.transaction_service import TransactionService
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.schemas.bulk_import import ImportResult
from app.core.exceptions import NotFoundError

router = APIRouter()

TEMPLATE_CSV = """date,amount,type,category,account,description
2026-01-15,50000,expense,Food,Personal,Lunch at restaurant
2026-01-16,2000000,income,Salary,Personal,Monthly salary
2026-01-17,30000,expense,Transport,Shared,Bus tickets
2026-01-18,15000,expense,Entertainment,Shared,Movie night
"""


def get_controller(db: Session = Depends(get_db)) -> TransactionController:
    repository = TransactionRepository(db)
    service    = TransactionService(repository)
    return TransactionController(service, db)


@router.get("/transactions", response_model=List[TransactionResponse])
def list_transactions(
    type: Optional[str] = Query(default=None),
    category_id: Optional[UUID] = Query(default=None),
    account_id: Optional[UUID] = Query(default=None),
    controller: TransactionController = Depends(get_controller),
    current_user=Depends(get_current_user),
):
    return controller.list_transactions(
        type=type,
        category_id=category_id,
        account_id=account_id,
        user_id=current_user.id
    )


@router.post("/transactions", response_model=TransactionResponse)
def create_transaction(
    data: TransactionCreate,
    controller: TransactionController = Depends(get_controller),
    current_user=Depends(get_current_user)
):
    return controller.create_transaction(data, current_user)


@router.get("/transactions/import/template", response_class=PlainTextResponse)
def download_template():
    return PlainTextResponse(
        content=TEMPLATE_CSV,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=import_template.csv"}
    )


@router.post("/transactions/import", response_model=ImportResult)
async def import_transactions(
    file: UploadFile = File(...),
    controller: TransactionController = Depends(get_controller),
    current_user=Depends(get_current_user)
):
    if not any(file.filename.lower().endswith(ext) for ext in (".csv", ".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Unsupported format. Use .csv or .xlsx")
    try:
        return await controller.import_transactions(file, current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

raise NotFoundError("Transaction")