import asyncio
import random
from decimal import Decimal

from src.models.base_models import Account
from src.repositories.account_repository import account_repository
from src.schemas.custom import ActuallyBalanceDTO, TargetAccountDTO
from src.schemas.account_schema import AccountDTO, AccountAddDTO
from src.services.exceptions import BusinessError
from src.services.decorator import validate_phone_number


class AccountService:

    @staticmethod
    async def generate_random_account_number() -> str:
        """
        Метод генерирует случайный номер счёта состоящий из 20 цифр
        для физ лица.
        :return: str
        """
        prefix = "40817"
        remaining_digits = "".join([str(random.randint(0, 9)) for _ in range(15)])
        acc_number = prefix + remaining_digits
        return acc_number

    @staticmethod
    async def validate_account(account: AccountAddDTO) -> AccountDTO | None:
        """
        Метод принимает данные извне, распаковывает в модель Account
        и передаёт её в репозиторий методу create_account_in_db.
        Метод create_account_in_db возвращает обратно модель Account
        для преобразования в DTO.
        :param account: AccountAddDTO
        :return: list[AccountDTO] | None
        """
        model_account = Account(**account.model_dump())
        added_account = await account_repository.create_account_in_db(model_account)
        if added_account:
            result_dto = AccountDTO.model_validate(added_account, from_attributes=True)
            return result_dto
        return None

    @staticmethod
    async def validate_account_info(user_id: int) -> list[AccountDTO] | None:
        """
        Метод принимает модель Account из репозитория от
        метода get_account_info и преобразует её в модель DTO.
        :return: list[AccountDTO] | None
        """
        model_account = await account_repository.get_account_info(user_id)
        if model_account:
            result_dto = [
                AccountDTO.model_validate(model_account, from_attributes=True)
            ]
            return result_dto
        return None

    @staticmethod
    async def validate_actual_balance(user_id: int) -> list[ActuallyBalanceDTO] | None:
        """
        Метод принимает строку результирующего набора из репозитория от
        метода get_account_info и преобразует её в модель DTO.
        :return: list[ActuallyBalanceDTO] | None
        """
        actual_balance = await account_repository.get_actual_balance(user_id)
        if actual_balance:
            result_dto = [
                ActuallyBalanceDTO.model_validate(row, from_attributes=True)
                for row in actual_balance
            ]
            return result_dto
        return None

    @staticmethod
    @validate_phone_number
    async def validate_target_account(phone_number: str) -> list[TargetAccountDTO] | None:
        """
        Метод принимает номер телефона и передаёт его в метод
        get_target_account для получения счёта получателя.
        После возврата из репозитория модели счёта получателя,
        модель преобразуется в DTO.
        :param phone_number: str
        :return: list[TargetAccountDTO] | None
        """
        model_account = await account_repository.get_target_account(phone_number)
        if model_account:
            result_dto = [
                TargetAccountDTO.model_validate(row, from_attributes=True)
                for row in model_account
            ]
            return result_dto
        return None

    @staticmethod
    async def response_top_up_balance(
        account_id: int, card_number: str, amount: Decimal
    ) -> bool | None:
        """
        Метод проверяет валидность поля 'amount' от пользователя
        для метода top_up_balance в репозитории.
        В случае, если amount меньше нуля, то вызывается
        исключение ValueError, иначе amount передаётся
        в репозиторий.
        :param card_number: str
        :param account_id: int
        :param amount: Decimal
        :return: bool | None
        """
        if amount <= Decimal("0.00"):
            raise BusinessError(
                message="Amount must be greater or equal to 0",
                error_code="INVALID_AMOUNT",
            )
        return await account_repository.top_up_balance(account_id, card_number, amount)

    @staticmethod
    async def response_transfer_money(
        target_card_number: str,
        target_account_id: int,
        card_number: str,
        account_id: int,
        amount: Decimal,
    ) -> bool | None:
        """
        Метод проверяет валидность полей 'phone_number' и
        'amount' от пользователя.
        В случае, если одна из проверок не прошла,
        вызывается исключение ValueError.
        Иначе аргументы отправляются в метод transfer_money
        :param target_account_id: str
        :param target_card_number: str
        :param card_number: str
        :param account_id: int
        :param amount: Decimal
        :return: bool | None
        """
        if amount <= Decimal("0.00"):
            raise BusinessError(
                message="Amount must be greater or equal to 0",
                error_code="INVALID_AMOUNT",
            )
        return await account_repository.transfer_money(
            target_card_number,
            target_account_id,
            card_number,
            account_id,
            amount,
        )


account_service = AccountService()
