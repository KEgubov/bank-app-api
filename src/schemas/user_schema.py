from pydantic import BaseModel, Field, field_validator, EmailStr


class UserAddDTO(BaseModel):
    first_name: str = Field(min_length=1, max_length=50, description="First name")
    last_name: str = Field(min_length=1, max_length=50, description="Last name")
    super_last_name: str = Field(
        min_length=1, max_length=50, description="Super last name"
    )
    phone_number: str = Field(min_length=10, max_length=20, description="Phone Number")
    password: str = Field(min_length=7, max_length=20, description="Password")
    email: EmailStr = Field(min_length=10, max_length=50, description="Email address")

    @field_validator("phone_number")
    @classmethod
    def validate_login(cls, v):
        if v.isalpha():
            raise ValueError("Phone number must be alphanumeric")
        if "+" not in v:
            raise ValueError("Phone number must be valid")
        return v


class UserDTO(UserAddDTO):
    user_id: int
