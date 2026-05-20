from typing import Any

from fastapi import APIRouter, HTTPException

from src.api.dependencies import CurrentUserDep
from src.schemas.card_schema import CardAddDTO
from src.services.card_service import card_service

router = APIRouter(prefix="/bank_app/v1/cards", tags=["Card"])


@router.post("/")
async def add_card(
    card_dto: CardAddDTO, current_user: CurrentUserDep
) -> dict[str, bool | Any]:
    """
    Эндпоинт принимает данные для добавления карты.
    account_id и phone_number вводятся автоматически
    из текущего пользователя при аутентификации.
    :param card_dto: CardAddDTO
    :param current_user: CurrentUserDep
    :return: dict[str, bool | Any]
    """
    card_dto.account_id = current_user.account_id
    card_dto.phone_number = current_user.phone_number
    data_card = await card_service.validate_card_data(card_dto)
    if not data_card:
        raise HTTPException(status_code=409, detail="Card already exists")
    return {"success": True, "card": data_card}


@router.get("/number")
async def card_number(current_user: CurrentUserDep) -> dict[str, bool | Any]:
    number = await card_service.validate_card_number(current_user.card_number)
    if not number:
        raise HTTPException(status_code=404, detail="Card number not found")
    return {"success": True, "number": number[0]}


@router.get("/all")
async def all_cards(current_user: CurrentUserDep) -> dict[str, bool | Any]:
    """
    Эндпоинт получает все имеющиеся карты пользователя.
    В случае отсутствия карт возвращает пустой список.
    :param current_user: CurrentUserDep
    :return: dict[str, bool | Any]
    """
    card_list = await card_service.validate_all_cards_from_account(
        current_user.account_id
    )
    if not card_list:
        return {"success": False, "account": card_list[0]}
    return {"success": True, "account": card_list[0]}


@router.get("/search")
async def find_user_card(current_user: CurrentUserDep) -> bool:
    response = await card_service.response_find_card(current_user.card_number)
    return response
