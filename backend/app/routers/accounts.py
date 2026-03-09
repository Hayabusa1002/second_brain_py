from fastapi import APIRouter
from app.controllers.account_controller import AccountController

router = APIRouter()
controller = AccountController()

@router.get("/accounts/{account_id}/balance")
def get_balance(account_id):
    return controller.get_balance(account_id)