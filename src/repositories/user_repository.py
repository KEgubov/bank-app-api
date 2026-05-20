from sqlalchemy import select, Row
from sqlalchemy.exc import IntegrityError

from src.core.database import async_session
from src.models.base_models import User, Account, Card
from src.repositories.base_repository import BaseRepository
from src.repositories.exceptions import DuplicateError


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    @staticmethod
    async def create_user_in_db(user: User) -> User | None:
        async with async_session() as session:
            try:
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
            except IntegrityError as e:
                if "already exists" in str(e.orig):
                    raise DuplicateError(
                        message="User already exists",
                        error_code="USER_DUPLICATE",
                    )

    @staticmethod
    async def get_current_user_in_db(user_id: int) -> Row[tuple[int, str]] | None:
        async with async_session() as session:
            query = (
                select(
                    User.user_id,
                    User.phone_number,
                    Account.account_id,
                    Card.card_number,
                )
                .join(Account, onclause=(User.user_id == Account.user_id), isouter=True)
                .join(
                    Card, onclause=(Account.account_id == Card.account_id), isouter=True
                )
                .where(User.user_id == user_id)
            )
            result = await session.execute(query)
            return result.first() if result else None

    @staticmethod
    async def get_target_name(phone_number: str) -> Row[tuple[str]] | None:
        """
        Принимает номер телефона от пользователя при переводе ДС,
        возвращает имя получателя.
        :param phone_number : str
        :return: list[FirstLastSuperName] | bool
        """
        async with async_session() as session:
            query = select(
                User.user_id, User.first_name, User.last_name, User.super_last_name
            ).where(User.phone_number == phone_number)
            target_name = await session.execute(query)
            return target_name.first()

    @staticmethod
    async def get_user_profile(user_id: int) -> list[User] | None:
        """
        Получает всю информацию о пользователе
        :return: list[User] | None
        """
        async with async_session() as session:
            query = select(User).where(User.user_id == user_id)
            model_user = await session.execute(query)
            return model_user.scalar_one()

    @staticmethod
    async def get_find_owner_name(user_id: int) -> Row[tuple[int, str]] | None:
        """
        Метод используется при выводе информации о счёте.
        Получает ФИО для информации о владельце счёта
        :return: list[FirstLastSuperNameDTO] | None
        """
        async with async_session() as session:
            query = select(
                User.user_id,
                User.first_name,
                User.last_name,
                User.super_last_name,
            ).where(User.user_id == user_id)
            owner_name = await session.execute(query)
            return owner_name.first()


user_repository = UserRepository()
