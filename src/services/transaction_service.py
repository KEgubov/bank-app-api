from src.repositories.transaction_repository import txn_repository
from src.schemas.relationships import AccountTransactionRelDTO


class TransactionService:

    @staticmethod
    async def valid_all_txn(
        account_id: int,
    ) -> list[AccountTransactionRelDTO] | None:
        """
        Метод получает все транзакции по счету из БД
        и конвертирует их в Pydantic модель.
        :param account_id: int
        :return: list[AccountTransactionRelDTO] | None
        """
        all_txn = await txn_repository.get_all_txn(account_id)
        if all_txn:
            result_dto = [
                AccountTransactionRelDTO.model_validate(row, from_attributes=True)
                for row in all_txn
            ]
            return result_dto
        return None


txn_service = TransactionService()
