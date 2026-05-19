import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class TransactionDTO(BaseModel):
    txn_type: str
    amount: Decimal
    txn_date: Optional[datetime.datetime] = None
    card_number: Optional[str] = None