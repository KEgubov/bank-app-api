from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.core.database import async_session
from src.models.base_models import Transaction, Account
from src.repositories.base_repository import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self):
        super().__init__(Transaction)

    @staticmethod
    async def get_all_txn(account_id: int) -> list[Transaction] | None:
        """
        Получает список всех транзакций со счёта пользователя.
        Метод использует selectinload для one to many связи.
        :param account_id: int
        :return: List[Transaction] | None
        """
        async with async_session() as session:
            query = (
                select(Account)
                .options(selectinload(Account.transaction))
                .where(Account.account_id == account_id)
            )
            all_txn = await session.execute(query)
            return all_txn.unique().scalars().all() if all_txn else None

txn_repository = TransactionRepository()