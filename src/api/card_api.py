from typing import Any

from fastapi import APIRouter, HTTPException

from src.api.dependencies import CurrentUserDep
from src.schemas.card_schema import CardAddDTO
from src.services.card_service import card_service

router = APIRouter(prefix="/bank_app/v1/cards", tags=["Card"])


@router.post("/add")
def add_card(
    card_dto: CardAddDTO, current_user: CurrentUserDep
) -> dict[str, bool | Any]:
    card_dto.account_id = current_user.account_id
    card_dto.phone_number = current_user.phone_number
    data_card = card_service.validate_card_data(card_dto)
    if not data_card:
        raise HTTPException(status_code=409, detail="Card already exists")
    return {"success": True, "card": data_card}


@router.get("/number")
def card_number(current_user: CurrentUserDep) -> dict[str, bool | Any]:
    number = card_service.validate_card_number(current_user.card_number)
    if not number:
        raise HTTPException(status_code=404, detail="Card number not found")
    return {"success": True, "number": number}


@router.get("/all")
def all_cards(current_user: CurrentUserDep) -> dict[str, bool | Any]:
    card_list = card_service.validate_all_cards_from_account(current_user.account_id)
    if not card_list:
        raise HTTPException(status_code=404, detail="Card number not found")
    return {"success": True, "cards": card_list}


@router.get("/find")
def find_user_card(current_user: CurrentUserDep) -> bool:
    response = card_service.response_find_card(current_user.card_number)
    return response
