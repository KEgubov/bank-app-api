from src.schemas import UserDTO, AccountDTO, ContactDTO, TransactionDTO, CardDTO


class UserContactRelDTO(UserDTO):
    """
    Используется для конвертации полученных данных в методе
    get_all_contacts_from_user. На выходе получается вложенная
    структура, где 1 пользователь и его контакты (rel one to many)
    """

    contact: list["ContactDTO"]


class AccountCardRelDTO(AccountDTO):
    """
    Используется для конвертации полученных данных в методе
    get_all_cards_from_account. На выходе получается вложенная
    структура, где 1 аккаунт и все привязанные карты (rel one to many)
    """

    card: list["CardDTO"]


class AccountTransactionRelDTO(AccountDTO):
    """
    Используется для конвертации полученных данных в методе
    get_all_txn_from_account. На выходе получается вложенная
    структура, где 1 аккаунт и все транзакции по счёту (rel one to many)
    """

    transaction: list["TransactionDTO"]


class UserAccountRelDTO(AccountDTO):
    account: "AccountDTO"


class CardRelDTO(CardDTO):
    account: "AccountDTO"


class TransactionRelDTO(TransactionDTO):
    account: "AccountDTO"
