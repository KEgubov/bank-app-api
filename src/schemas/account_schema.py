import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class AccountAddDTO(BaseModel):
    user_id: int
    account_number: str = Field(
        min_length=20, max_length=20, description="Account number"
    )


class AccountDTO(AccountAddDTO):
    account_id: int
    user_id: int
    total_operations: int
    balance: Decimal
    last_activity_date: Optional[datetime.datetime] = None