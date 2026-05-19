from typing import Any

from fastapi import APIRouter, HTTPException

from src.api.dependencies import CurrentUserDep
from src.services.user_service import user_service

router = APIRouter(prefix="/bank_app/v1/users", tags=["User"])


@router.get("/name/{phone_number}")
async def get_user_by_phone(
    phone_number: str, current_user: CurrentUserDep
) -> dict[str, bool | Any]:
    name = await user_service.validate_target_name(phone_number)
    if not name:
        raise HTTPException(status_code=400, detail="Invalid phone number")
    return {"success": True, "user_data": name}


@router.get("/me")
async def user_profile(current_user: CurrentUserDep) -> dict[str, bool | Any]:
    profile = await user_service.validate_user_profile(current_user.user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "user": profile}


@router.get("/owner")
async def get_owner_name(current_user: CurrentUserDep) -> dict[str, bool | Any]:
    name = await user_service.validate_owner_name(current_user.user_id)
    if not name:
        raise HTTPException(status_code=404, detail="Owner name not found")
    return {"success": True, "owner_name": name}
