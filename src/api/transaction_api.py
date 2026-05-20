from typing import Any

from fastapi import APIRouter

from src.api.dependencies import CurrentUserDep
from src.services.transaction_service import txn_service

router = APIRouter(prefix="/bank_app/v1/history", tags=["Transaction"])


@router.get("/")
async def get_all_txn_from_account(
    current_user: CurrentUserDep,
) -> dict[str, bool | Any]:
    all_txn = await txn_service.valid_all_txn(current_user.account_id)
    if not all_txn:
        return {"success": False, "message": "No transactions found."}
    return {"success": True, "all_txn": all_txn}
