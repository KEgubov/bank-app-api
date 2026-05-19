import functools
from typing import Coroutine, Callable

from src.services.exceptions import BusinessError


def validate_phone_number(coroutine: Callable) -> Coroutine:
    """
    Декоратор для валидации входящих значений номера телефона
    от пользователя
    :return: Callable
    """
    @functools.wraps(coroutine)
    async def inner(phone_number: str):
        if len(phone_number) != 12:
            raise BusinessError(
                message="Invalid phone number", error_code="INVALID_PHONE_NUMBER"
            )
        elif phone_number.isalpha():
            raise BusinessError(
                message="Phone number must be alphanumeric",
                error_code="INVALID_PHONE_NUMBER",
            )
        elif "+" not in phone_number:
            raise BusinessError(
                message="Phone number must be valid",
                error_code="INVALID_PHONE_NUMBER",
            )
        return await coroutine(phone_number)
    return inner
