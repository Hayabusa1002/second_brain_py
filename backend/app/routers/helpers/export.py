from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload

from app.db.deps import get_current_user, get_db
from app.models.transaction import Transaction
from app.services.helpers.export_service import ExportService


router = APIRouter(
    prefix="/export",
    tags=["export"],
    dependencies=[Depends(get_current_user)],
)


def _get_enriched_transactions(
    db: Session,
    user_id: UUID,
    type: Optional[str] = None,
    category_id: Optional[UUID] = None,
    account_id: Optional[UUID] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    q: Optional[str] = None,
):
    query = (
        db.query(Transaction)
        .options(
            joinedload(Transaction.account),
            joinedload(Transaction.category),
        )
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


def _export(
    fmt: str,
    filename: str,
    db: Session,
    current_user,
    type: Optional[str],
    category_id: Optional[UUID],
    account_id: Optional[UUID],
    date_from: Optional[date],
    date_to: Optional[date],
    q: Optional[str],
) -> Response:
    txs = _get_enriched_transactions(
        db=db,
        user_id=current_user.id,
        type=type,
        category_id=category_id,
        account_id=account_id,
        date_from=date_from,
        date_to=date_to,
        q=q,
    )

    exporter = ExportService()

    if fmt == "json":
        content = exporter.to_json(txs)
        media_type = "application/json"
    elif fmt == "csv":
        content = exporter.to_csv(txs)
        media_type = "text/csv"
    elif fmt == "xlsx":
        content = exporter.to_xlsx(txs)
        media_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    elif fmt == "pdf":
        content = exporter.to_pdf(txs)
        media_type = "application/pdf"
    else:
        raise ValueError("Unsupported export format")

    return Response(
        content=content,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.get("/json")
def export_json(
    type: Optional[str] = Query(default=None),
    category_id: Optional[UUID] = Query(default=None),
    account_id: Optional[UUID] = Query(default=None),
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
    q: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return _export(
        fmt="json",
        filename="transactions.json",
        db=db,
        current_user=current_user,
        type=type,
        category_id=category_id,
        account_id=account_id,
        date_from=date_from,
        date_to=date_to,
        q=q,
    )


@router.get("/csv")
def export_csv(
    type: Optional[str] = Query(default=None),
    category_id: Optional[UUID] = Query(default=None),
    account_id: Optional[UUID] = Query(default=None),
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
    q: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return _export(
        fmt="csv",
        filename="transactions.csv",
        db=db,
        current_user=current_user,
        type=type,
        category_id=category_id,
        account_id=account_id,
        date_from=date_from,
        date_to=date_to,
        q=q,
    )


@router.get("/xlsx")
def export_xlsx(
    type: Optional[str] = Query(default=None),
    category_id: Optional[UUID] = Query(default=None),
    account_id: Optional[UUID] = Query(default=None),
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
    q: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return _export(
        fmt="xlsx",
        filename="transactions.xlsx",
        db=db,
        current_user=current_user,
        type=type,
        category_id=category_id,
        account_id=account_id,
        date_from=date_from,
        date_to=date_to,
        q=q,
    )


@router.get("/pdf")
def export_pdf(
    type: Optional[str] = Query(default=None),
    category_id: Optional[UUID] = Query(default=None),
    account_id: Optional[UUID] = Query(default=None),
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
    q: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return _export(
        fmt="pdf",
        filename="transactions.pdf",
        db=db,
        current_user=current_user,
        type=type,
        category_id=category_id,
        account_id=account_id,
        date_from=date_from,
        date_to=date_to,
        q=q,
    )