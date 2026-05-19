from typing import Annotated

from authx import TokenPayload
from fastapi import HTTPException
from fastapi.params import Depends

from src.configs.auth_config import security
from src.schemas.custom import CurrentUserDTO
from src.services.user_service import user_service


def get_current_user(
    payload: TokenPayload = Depends(security.access_token_required),
) -> CurrentUserDTO:
    user = user_service.validate_current_user(user_id=int(payload.sub))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


CurrentUserDep = Annotated[CurrentUserDTO, Depends(get_current_user)]
