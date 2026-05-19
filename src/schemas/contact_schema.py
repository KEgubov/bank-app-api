from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ContactAddDTO(BaseModel):
    phone_number: str = Field(
        min_length=12, max_length=20, description="Phone number"
    )


    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        if v.isalpha():
            raise ValueError("Phone number must be alphanumeric")
        if "+" not in v:
            raise ValueError("Phone number must be valid")
        return v


class ContactDTO(ContactAddDTO):
    user_id: Optional[int] = None
    contact_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    super_last_name: Optional[str] = None