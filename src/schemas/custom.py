from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ActuallyBalanceDTO(BaseModel):
    """
    Используется для конвертации полученных данных в методе
    get_actual_balance.
    """

    balance: Decimal


class FirstLastSuperNameDTO(BaseModel):
    """
    Используется для конвертации полученных данных в методах
    get_target_name и get_find_owner_name.
    """

    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    super_last_name: Optional[str] = None


class CurrentUserDTO(BaseModel):
    user_id: int
    phone_number: str
    account_id: Optional[int] = None
    card_number: Optional[str] = None


class TargetAccountDTO(BaseModel):
    account_id: int
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    super_last_name: Optional[str] = None
    card_number: Optional[str] = None


class CardNumberDTO(BaseModel):
    card_number: str


class LoginData(BaseModel):
    phone_number: str = Field(min_length=10, max_length=20, description="Phone number")
    password: str = Field(min_length=7, max_length=20, description="Password")

class UserIDDTO(BaseModel):
    user_id: int
