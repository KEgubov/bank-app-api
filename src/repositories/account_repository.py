import datetime
from decimal import Decimal

from sqlalchemy import select, update, insert, Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from src.core.database import async_session
from src.models.base_models import Account, User, Transaction, TxnType, Card
from src.repositories.base_repository import BaseRepository


class AccountRepository(BaseRepository[Account]):
    def __init__(self):
        super().__init__(Account)

    @staticmethod
    async def create_account_in_db(account: Account) -> Account:
        """
        Метод принимает модель Account с сервиса
        от метода validate_account, добавляет объект в сессию
        и фиксирует изменения в базе данных.
        Производит refresh для возврата модели обратно в сервис
        методу validate_account для преобразования модели в DTO.
        :param account: Account
        :return: Account
        """
        async with async_session() as session:
            session.add(account)
            await session.commit()
            await session.refresh(account)
            return account

    @staticmethod
    async def get_account_info(user_id: int) -> Account | None:
        """
        Получает информация о счёте пользователя.
        Метод использует joinedload для one to one связи.
        :return: Account | None
        """
        async with async_session() as session:
            query = (
                select(User)
                .options(joinedload(User.account))
                .where(User.user_id == user_id)
            )
            result = await session.execute(query)
            user = result.unique().scalar_one_or_none()
            return user.account if user else None

    @staticmethod
    async def get_actual_balance(user_id: int) -> Row[tuple[Decimal]] | None:
        """
        Получает актуальный баланс счёта.
        :return: Row[tuple[Decimal]]
        """
        async with async_session() as session:
            query = (
                select(Account.balance)
                .join(User, User.user_id == Account.user_id)
                .where(User.user_id == user_id)
            )
            actual_balance = await session.execute(query)
            return actual_balance.all()

    @staticmethod
    async def get_target_account(phone_number: str) -> Row[tuple[str, int]] | None:
        """
        Получает счёт по номеру телефона.
        Метод используется при переводе ДС с одного аккаунта
        на другой.
        :param phone_number: str
        :return: Row[tuple[str, int]] | None
        """
        async with async_session() as session:
            query = (
                select(
                    User.first_name,
                    User.last_name,
                    User.super_last_name,
                    Account.account_id,
                    Account.user_id,
                    Card.card_number,
                )
                .join(User, User.user_id == Account.user_id, isouter=True)
                .join(Card, Account.account_id == Card.account_id, isouter=True)
                .where(User.phone_number == phone_number)
            )
            model_account = await session.execute(query)
            return model_account.all()

    @staticmethod
    async def top_up_balance(
        account_id: int, card_number: str, amount: Decimal
    ) -> bool | None:
        """
        Пополнение собственного счёта.
        :param card_number: str
        :param account_id: int
        :param amount: Decimal
        :return: bool | None
        """
        async with async_session() as session:
            try:
                stmt_top_up = (
                    update(Account)
                    .where(Account.account_id == account_id)
                    .values(
                        balance=Account.balance + amount,
                        total_operations=Account.total_operations + 1,
                        last_activity_date=datetime.datetime.now(),
                    )
                )
                await session.execute(stmt_top_up)

                stmt_insert_in_txn = insert(Transaction).values(
                    account_id=account_id,
                    card_number=card_number,
                    txn_type=TxnType.C,
                    amount=amount,
                )
                await session.execute(stmt_insert_in_txn)
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                return False
            except Exception:
                await session.rollback()
                return False

    @staticmethod
    async def transfer_money(
        target_card_number: str,
        target_account_id: int,
        card_number: str,
        account_id: int,
        amount: Decimal,
    ) -> bool | None:
        """
        Перевод по номеру телефона с указанием суммы.
        При вводе номера телефона делается запрос на наличие
        счёта получателя, если счёт имеется, то происходит снятие
        ДС и зачисление их на счёт получателя с записью об
        операциях в таблицу Transaction.
        :param target_account_id: str
        :param target_card_number: str
        :param card_number: str
        :param account_id: int
        :param amount: Decimal
        :return: bool | None
        """
        async with async_session() as session:
            try:
                stmt_debit = (
                    update(Account)
                    .where(Account.account_id == account_id)
                    .values(
                        balance=Account.balance - amount,
                        total_operations=Account.total_operations + 1,
                        last_activity_date=datetime.datetime.now(),
                    )
                )
                await session.execute(stmt_debit)

                stmt_curr_txn = insert(Transaction).values(
                    account_id=account_id,
                    card_number=card_number,
                    txn_type=TxnType.D,
                    amount=amount,
                )
                await session.execute(stmt_curr_txn)

                stmt_targ_credit = (
                    update(Account)
                    .where(Account.account_id == target_account_id)
                    .values(
                        balance=Account.balance + amount,
                        total_operations=Account.total_operations + 1,
                        last_activity_date=datetime.datetime.now(),
                    )
                )
                await session.execute(stmt_targ_credit)

                stmt_targ_txn = insert(Transaction).values(
                    account_id=target_account_id,
                    card_number=target_card_number,
                    txn_type=TxnType.C,
                    amount=amount,
                )
                await session.execute(stmt_targ_txn)
                await session.commit()
                return True
            except IntegrityError as e:
                await session.rollback()
            except Exception as e:
                await session.rollback()


account_repository = AccountRepository()
