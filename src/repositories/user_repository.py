from sqlalchemy import select, Row

from src.core.database import session_factory
from src.models.base_models import User, Account, Card
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    @staticmethod
    def create_user_in_db(user: User) -> User:
        with session_factory() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    @staticmethod
    def get_current_user_in_db(user_id: int) -> Row[tuple[int, str]] | None:
        with session_factory() as session:
            query = (
                select(User.user_id, User.phone_number, Account.account_id, Card.card_number)
                .join(Account, onclause=(User.user_id == Account.user_id), isouter=True)
                .join(Card, onclause=(Account.account_id == Card.account_id), isouter=True)
                .where(User.user_id == user_id)
            )
            result = session.execute(query).first()
            return result if result else None



    @staticmethod
    def get_target_name(phone_number: str) -> Row[tuple[str]] | None:
        """
        Принимает номер телефона от пользователя при переводе ДС,
        возвращает имя получателя.
        :param phone_number : str
        :return: list[FirstLastSuperName] | bool
        """
        with session_factory() as session:
            query = select(
                User.user_id, User.first_name, User.last_name, User.super_last_name
            ).where(User.phone_number == phone_number)
            target_name = session.execute(query).all()
            return target_name

    @staticmethod
    def get_user_profile(user_id: int) -> list[User] | None:
        """
        Получает всю информацию о пользователе
        :return: list[User] | None
        """
        with session_factory() as session:
            query = select(User).where(User.user_id == user_id)
            model_user = session.execute(query).scalars().all()
            return model_user

    @staticmethod
    def get_find_owner_name(user_id: int) -> Row[tuple[int, str]] | None:
        """
        Метод используется при выводе информации о счёте.
        Получает ФИО для информации о владельце счёта
        :return: list[FirstLastSuperNameDTO] | None
        """
        with session_factory() as session:
            query = select(
                User.user_id,
                User.first_name,
                User.last_name,
                User.super_last_name,
            ).where(User.user_id == user_id)
            owner_name = session.execute(query).all()
            return owner_name


user_repository = UserRepository()
