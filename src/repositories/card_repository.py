from sqlalchemy import select, Row
from sqlalchemy.orm import selectinload

from src.core.database import async_session
from src.models.base_models import Card, Account
from src.repositories.base_repository import BaseRepository


class CardRepository(BaseRepository[Card]):
    def __init__(self):
        super().__init__(Card)

    @staticmethod
    async def create_card_in_db(card: Card) -> Card:
        async with async_session() as session:
            session.add(card)
            await session.commit()
            await session.refresh(card)
            return card

    @staticmethod
    async def get_card_number(card_number: str) -> Row[tuple[str]] | None:
        """
        Получение номера карты текущего пользователя.
        :param card_number: str
        :return: Row[tuple[str]] | None
        """
        async with async_session() as session:
            query = select(Card.card_number).where(
                Card.card_number == card_number
            )
            card_number = await session.execute(query)
            return card_number.all() if card_number else None

    @staticmethod
    async def get_all_cards_from_account(account_id: int) -> list[Account] | None:
        """
        Получает все карты из счёта пользователя.
        Метод использует selectinload для one to many связи.
        :param account_id: int
        :return: list[Account]
        """
        async with async_session() as session:
            query = (
                select(Account)
                .options(selectinload(Account.card))
                .where(Account.account_id == account_id)
            )
            all_cards = await session.execute(query)
            return all_cards.unique().scalars().all() if all_cards else None

    @staticmethod
    async def find_card(card_number: str) -> bool:
        """
        Поиск карты текущего пользователя.
        :param card_number: str
        :return: bool
        """
        async with async_session() as session:
            query = (
                select(Card)
                .where(Card.card_number == card_number)
            )
            result = await session.execute(query)
            return True if result.first() else False


card_repository = CardRepository()
