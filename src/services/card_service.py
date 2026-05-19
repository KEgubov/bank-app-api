from src.models.base_models import Card
from src.repositories.card_repository import card_repository
from src.schemas.card_schema import CardAddDTO, CardDTO
from src.schemas.custom import CardNumberDTO
from src.schemas.relationships import AccountCardRelDTO


class CardService:

    @staticmethod
    async def validate_card_data(card: CardAddDTO) -> list[CardDTO] | None:
        model_card = Card(**card.model_dump())
        added_card = await card_repository.create_card_in_db(model_card)
        if added_card:
            result_dto = [CardDTO.model_validate(added_card, from_attributes=True)]
            return result_dto
        return None

    @staticmethod
    async def validate_card_number(card_number: str) -> list[CardNumberDTO] | None:
        card_number = await card_repository.get_card_number(card_number)
        if card_number:
            result_dto = [
                CardNumberDTO.model_validate(row, from_attributes=True)
                for row in card_number
            ]
            return result_dto
        return None

    @staticmethod
    async def validate_all_cards_from_account(
        account_id: int,
    ) -> list[AccountCardRelDTO] | None:
        all_cards = await card_repository.get_all_cards_from_account(account_id)
        if all_cards:
            result_dto = [
                AccountCardRelDTO.model_validate(row, from_attributes=True)
                for row in all_cards
            ]
            return result_dto
        return None

    @staticmethod
    async def response_find_card(card_number: str) -> bool:
        return await card_repository.find_card(card_number)


card_service = CardService()
