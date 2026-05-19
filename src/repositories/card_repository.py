from sqlalchemy import select, Row
from sqlalchemy.orm import selectinload

from src.core.database import session_factory
from src.models.base_models import Card, Account
from src.repositories.base_repository import BaseRepository


class CardRepository(BaseRepository[Card]):
    def __init__(self):
        super().__init__(Card)

    @staticmethod
    def create_card_in_db(card: Card) -> Card:
        with session_factory() as session:
            session.add(card)
            session.commit()
            session.refresh(card)
            return card

    @staticmethod
    def get_card_number(card_number: str) -> Row[tuple[str]] | None:
        """
        Получение номера карты текущего пользователя.
        :param card_number: str
        :return: Row[tuple[str]] | None
        """
        with session_factory() as session:
            query = select(Card.card_number).where(
                Card.card_number == card_number
            )
            card_number = session.execute(query).all()
            return card_number if card_number else None

    @staticmethod
    def get_all_cards_from_account(account_id: int) -> list[Account] | None:
        """
        Получает все карты из счёта пользователя.
        Метод использует selectinload для one to many связи.
        :param account_id: int
        :return: list[Account]
        """
        with session_factory() as session:
            query = (
                select(Account)
                .options(selectinload(Account.card))
                .where(Account.account_id == account_id)
            )
            all_cards = session.execute(query).unique().scalars().all()
            return all_cards if all_cards else None

    @staticmethod
    def find_card(card_number: str) -> bool:
        """
        Поиск карты текущего пользователя.
        :param card_number: str
        :return: bool
        """
        with session_factory() as session:
            query = (
                select(Card)
                .where(Card.card_number == card_number)
            )
            result = session.execute(query).first()
            return True if result else False


card_repository = CardRepository()
