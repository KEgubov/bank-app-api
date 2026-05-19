from typing import Any

from fastapi import APIRouter, HTTPException, Response

from src.configs.auth_config import security
from src.schemas.custom import LoginData
from src.schemas.user_schema import UserAddDTO
from src.services.auth_service import auth_service
from src.services.user_service import user_service

router = APIRouter(prefix="/bank_app/v1/welcome", tags=["Welcome"])

@router.post("/registration")
async def input_data_user(user: UserAddDTO) -> dict[str, bool | Any]:
    user = await user_service.validate_user(user)
    if not user:
        raise HTTPException(status_code=409, detail="User already registered")
    return {"success": True, "user": user}

@router.post("/login")
async def login(creds: LoginData, response: Response) -> dict[str, str]:
    user = await auth_service.resp_authenticate_user(creds)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = security.create_access_token(uid=str(user.user_id))
    response.set_cookie(security.config.JWT_ACCESS_COOKIE_NAME, token)
    return {"access_token": token}
