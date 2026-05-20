from decimal import Decimal
from typing import Any

from fastapi import APIRouter, HTTPException

from src.api.dependencies import CurrentUserDep
from src.schemas.account_schema import AccountAddDTO
from src.services.account_service import account_service

router = APIRouter(prefix="/bank_app/v1/accounts", tags=["Account"])


@router.post("/")
async def create_account(
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
    account_number = await account_service.generate_random_account_number()
    account_dto.user_id = current_user.user_id
    account_dto.account_number = account_number
    account = await account_service.validate_account(account_dto)
    return {"success": True, "account": account}


@router.get("/me")
async def get_my_account(
    current_user: CurrentUserDep,
) -> dict[str, bool] | dict[str, bool | Any]:
    """
    Информация о счёте пользователя.
    Эндпоинт получает ID пользователя после успешной
    аутентификации и передаёт его в сервис.
    :param current_user: CurrentUserDep
    :return: dict[str, bool | bool | Any]
    """
    info = await account_service.validate_account_info(current_user.user_id)
    if not info:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"success": True, "account_info": info[0]}


@router.get("/me/balance")
async def get_actual_balance_from_account(
    current_user: CurrentUserDep,
) -> dict[str, bool] | dict[str, bool | Any]:
    """
    Актуальный баланс счёта.
    Эндпоинт получает ID пользователя после успешной
    аутентификации и передаёт его в сервис.
    :param current_user: CurrentUserDep
    :return: dict[str, bool | bool | Any]
    """
    balance = await account_service.validate_actual_balance(current_user.user_id)
    return {"success": True, "balance": balance}


@router.patch("/me/top_up/{amount}")
async def top_up_account_balance(
    amount: Decimal, current_user: CurrentUserDep
) -> dict[str, bool] | dict[str, bool | Any]:
    top_up = await account_service.response_top_up_balance(
        current_user.account_id, current_user.card_number, amount
    )
    if not top_up:
        raise HTTPException(
            status_code=404, detail="Account not found"
        )
    return {"success": True}


@router.patch("/me/transfers")
async def account_transfer(
    phone_number: str, amount: Decimal, current_user: CurrentUserDep
) -> dict[str, bool | Any]:
    target_model = await account_service.validate_target_account(phone_number)
    if not target_model:
        raise HTTPException(status_code=404, detail="Account not found")
    transfer = await account_service.response_transfer_money(
        target_model[0].card_number,
        target_model[0].account_id,
        current_user.card_number,
        current_user.account_id,
        amount,
    )
    if not transfer:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"success": True, "transfer": transfer, "target_account": target_model[0]}
