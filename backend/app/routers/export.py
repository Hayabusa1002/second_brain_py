from typing import Optional
from uuid import UUID
from datetime import date
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.db.deps import get_db, get_current_user
from app.repositories.transaction_repository import TransactionRepository
from app.services.transaction_service import TransactionService
from app.services.export_service import ExportService

router = APIRouter()


def get_transactions(
    current_user,
    db: Session,
    type:        Optional[str]  = None,
    category_id: Optional[UUID] = None,
    account_id:  Optional[UUID] = None,
    date_from:   Optional[date] = None,
    date_to:     Optional[date] = None,
    q:           Optional[str]  = None,
):
    repo    = TransactionRepository(db)
    service = TransactionService(repo)
    return service.list_transactions(
        user_id=current_user.id,
        type=type,
        category_id=category_id,
        account_id=account_id,
        date_from=date_from,
        date_to=date_to,
        q=q,
    )


@router.get("/export/json")
def export_json(
    type:        Optional[str]  = Query(default=None),
    category_id: Optional[UUID] = Query(default=None),
    account_id:  Optional[UUID] = Query(default=None),
    date_from:   Optional[date] = Query(default=None),
    date_to:     Optional[date] = Query(default=None),
    q:           Optional[str]  = Query(default=None),
    db:          Session        = Depends(get_db),
    current_user                = Depends(get_current_user),
):
    txs  = get_transactions(current_user, db, type, category_id, account_id, date_from, date_to, q)
    data = ExportService().to_json(txs)
    return Response(
        content=data,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=transactions.json"},
    )


@router.get("/export/csv")
def export_csv(
    type:        Optional[str]  = Query(default=None),
    category_id: Optional[UUID] = Query(default=None),
    account_id:  Optional[UUID] = Query(default=None),
    date_from:   Optional[date] = Query(default=None),
    date_to:     Optional[date] = Query(default=None),
    q:           Optional[str]  = Query(default=None),
    db:          Session        = Depends(get_db),
    current_user                = Depends(get_current_user),
):
    txs  = get_transactions(current_user, db, type, category_id, account_id, date_from, date_to, q)
    data = ExportService().to_csv(txs)
    return Response(
        content=data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"},
    )


@router.get("/export/xlsx")
def export_xlsx(
    type:        Optional[str]  = Query(default=None),
    category_id: Optional[UUID] = Query(default=None),
    account_id:  Optional[UUID] = Query(default=None),
    date_from:   Optional[date] = Query(default=None),
    date_to:     Optional[date] = Query(default=None),
    q:           Optional[str]  = Query(default=None),
    db:          Session        = Depends(get_db),
    current_user                = Depends(get_current_user),
):
    txs  = get_transactions(current_user, db, type, category_id, account_id, date_from, date_to, q)
    data = ExportService().to_xlsx(txs)
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=transactions.xlsx"},
    )


@router.get("/export/pdf")
def export_pdf(
    type:        Optional[str]  = Query(default=None),
    category_id: Optional[UUID] = Query(default=None),
    account_id:  Optional[UUID] = Query(default=None),
    date_from:   Optional[date] = Query(default=None),
    date_to:     Optional[date] = Query(default=None),
    q:           Optional[str]  = Query(default=None),
    db:          Session        = Depends(get_db),
    current_user                = Depends(get_current_user),
):
    txs  = get_transactions(current_user, db, type, category_id, account_id, date_from, date_to, q)
    data = ExportService().to_pdf(txs)
    return Response(
        content=data,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=transactions.pdf"},
    )