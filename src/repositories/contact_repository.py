from sqlalchemy import select, Row, delete
from sqlalchemy.orm import selectinload

from src.core.database import session_factory
from src.models.base_models import Contact, User
from src.repositories.base_repository import BaseRepository


class ContactsRepository(BaseRepository[Contact]):
    def __init__(self):
        super().__init__(Contact)

    @staticmethod
    def create_contact_in_db(contact: Contact) -> Contact:
        """
        Создание контакта в базе данных
        :param contact:
        :return: Contact
        """
        with session_factory() as session:
            session.add(contact)
            session.commit()
            session.refresh(contact)
            return contact

    @staticmethod
    def find_user_by_phone_number(phone_number: str) -> Row[tuple[str]] | None:
        """
        Метод ищет пользователя в базе данных по номеру телефона
        и возвращает строку с ФИО и номером искомого контакта
        :param phone_number: str
        :return: Row[tuple[str]] | None
        """
        with session_factory() as session:
            query = (
                select(
                    User.first_name,
                    User.last_name,
                    User.super_last_name,
                    User.phone_number
                )
                .where(User.phone_number == phone_number)
            )
            user_model = session.execute(query).all()
            return user_model if user_model else None

    @staticmethod
    def get_all_contacts_from_user(user_id: int) -> list[User] | None:
        """
        Получает список контактов пользователя.
        Использует selectinload для one to many связи.
        :param user_id: int
        :return: List[User] | None
        """
        with session_factory() as session:
            query = (
                select(User)
                .options(selectinload(User.contact))
                .where(User.user_id == user_id)
            )
            all_contacts = session.execute(query).unique().scalars().all()
            return all_contacts if all_contacts else None

    @staticmethod
    def delete_contact_in_db(contact_id: int) -> bool:
        """
        Удаление контакта по ID
        :param contact_id: int
        :return: bool
        """
        with session_factory() as session:
            stmt = delete(Contact).where(Contact.contact_id == contact_id)
            res = session.execute(stmt)
            session.commit()
            return True if res else False


contact_repository = ContactsRepository()
