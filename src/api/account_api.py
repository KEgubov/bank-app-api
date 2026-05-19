from decimal import Decimal
from typing import Any

from fastapi import APIRouter, HTTPException

from src.api.dependencies import CurrentUserDep
from src.schemas.account_schema import AccountAddDTO
from src.services.account_service import account_service

router = APIRouter(prefix="/bank_app/v1/accounts", tags=["Account"])


@router.post("/create")
def input_data_account(
    account_dto: AccountAddDTO, current_user: CurrentUserDep
) -> dict[str, bool] | dict[str, bool | Any]:
    """
    Эндпоинт принимает id текущего пользователя,
    после успешной аутентификации и
    автоматически сгенерированный номер счёта
    из сервиса.
    Значения подставляются автоматически.
    :param account_dto: AccountAddDTO
    :param current_user: CurrentUserDep
    :return: dict[str, bool | bool | Any]
    """
    account_number = account_service.generate_random_account_number()
    account_dto.user_id = current_user.user_id
    account_dto.account_number = account_number
    account = account_service.validate_account(account_dto)
    if not account:
        return {"success": False}
    return {"success": True, "account": account}


@router.get("/info")
def account_info(
    current_user: CurrentUserDep,
) -> dict[str, bool] | dict[str, bool | Any]:
    """
    Информация о счёте пользователя.
    Эндпоинт получает ID пользователя после успешной
    аутентификации и передаёт его в сервис.
    :param current_user: CurrentUserDep
    :return: dict[str, bool | bool | Any]
    """
    info = account_service.validate_account_info(current_user.user_id)
    if not info:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"success": True, "account_info": info}


@router.get("/balance")
def get_actual_balance_from_account(
    current_user: CurrentUserDep,
) -> dict[str, bool] | dict[str, bool | Any]:
    """
    Актуальный баланс счёта.
    Эндпоинт получает ID пользователя после успешной
    аутентификации и передаёт его в сервис.
    :param current_user: CurrentUserDep
    :return: dict[str, bool | bool | Any]
    """
    balance = account_service.validate_actual_balance(current_user.user_id)
    return {"success": True, "balance": balance}


@router.patch("/top_up/{amount}")
def top_up_account_balance(
    amount: Decimal, current_user: CurrentUserDep
) -> dict[str, bool] | dict[str, bool | Any]:
    top_up = account_service.response_top_up_balance(
        current_user.account_id, current_user.card_number, amount
    )
    if not top_up:
        return {"success": False}
    return {"success": True}


@router.patch("/transfer/{phone_number}")
def account_transfer(
    phone_number: str, amount: Decimal, current_user: CurrentUserDep
) -> dict[str, bool | Any]:
    target_model = account_service.validate_target_account(phone_number)
    if not target_model:
        raise HTTPException(status_code=404, detail="Account not found")
    transfer = account_service.response_transfer_money(
        target_model[0].card_number,
        target_model[0].account_id,
        current_user.card_number,
        current_user.account_id,
        amount,
    )
    if not transfer:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"success": True, "transfer": transfer, "target_account": target_model}
