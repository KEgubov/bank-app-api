from pydantic import BaseModel, Field, field_validator


class CardAddDTO(BaseModel):
    account_id: int = Field(default=None, description="Account ID")
    card_number: str = Field(min_length=16, max_length=16, description="Card number")
    phone_number: str = Field(
        min_length=12, max_length=12, default=None, description="Phone number"
    )
    card_holder_name: str = Field(
        min_length=1, max_length=45, description="Card holder name"
    )
    valid_through_date: str = Field(
        min_length=5, max_length=5, description="Valid through date"
    )
    cvv2_cvc2_number: str = Field(
        min_length=3, max_length=3, description="Card CVV2 number"
    )

    @field_validator("card_number") #!!!!!!!!!!!!!!!!!!
    @classmethod
    def validate_card_number(cls, v):
        if not v.isdigit():
            raise ValueError("Card number must contain only digits")
        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        if v.isalpha():
            raise ValueError("Phone number must be alphanumeric")
        if "+" not in v:
            raise ValueError("Phone number must be valid")
        return v

    @field_validator("valid_through_date")
    @classmethod
    def validate_valid_through_date(cls, v):
        if not (len(v) == 5 and v[2] == "/"):
            raise ValueError("Valid through date must be in format: MM/YY")
        mm, yy = v.split("/")
        if not (mm.isdigit() and yy.isdigit()):
            raise ValueError("Month and year must be digits")
        if not (1 <= int(mm) <= 12):
            raise ValueError("Month and year must be between 1 and 12")
        return v


class CardDTO(CardAddDTO):
    pass