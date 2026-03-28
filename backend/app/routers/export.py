from typing import Optional
from uuid import UUID
from datetime import date
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload
from app.db.deps import get_db, get_current_user
from app.models.transaction import Transaction
from app.services.export_service import ExportService

router = APIRouter()

def _get_enriched_transactions(
    db: Session,
    user_id: UUID,
    type: Optional[str] = None,
    category_id: Optional[UUID] = None,
    account_id: Optional[UUID] = None,
    date_from=None,
    date_to=None,
    q: Optional[str] = None,
):
    query = (
        db.query(Transaction)
        .options(joinedload(Transaction.account), joinedload(Transaction.category))
        .filter(Transaction.created_by == user_id)
    )
    if type:
        query = query.filter(Transaction.type == type)
    if category_id:
        query = query.filter(Transaction.category_id == category_id)
    if account_id:
        query = query.filter(Transaction.account_id == account_id)
    if date_from:
        query = query.filter(Transaction.date >= date_from)
    if date_to:
        query = query.filter(Transaction.date <= date_to)
    if q:
        query = query.filter(Transaction.description.ilike(f"%{q}%"))
    return query.order_by(Transaction.date.desc()).all()


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
    txs = _get_enriched_transactions(db, current_user.id, type, category_id, account_id, date_from, date_to, q)
    data = ExportService().to_json(txs)
    return Response(content=data, media_type="application/json",
                    headers={"Content-Disposition": "attachment; filename=transactions.json"})


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
    txs = _get_enriched_transactions(db, current_user.id, type, category_id, account_id, date_from, date_to, q)
    data = ExportService().to_csv(txs)
    return Response(content=data, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=transactions.csv"})


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
    txs = _get_enriched_transactions(db, current_user.id, type, category_id, account_id, date_from, date_to, q)
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
    txs = _get_enriched_transactions(db, current_user.id, type, category_id, account_id, date_from, date_to, q)
    data = ExportService().to_pdf(txs)
    return Response(content=data, media_type="application/pdf",
                    headers={"Content-Disposition": "attachment; filename=transactions.pdf"})