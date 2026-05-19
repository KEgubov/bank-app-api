from typing import Any

from fastapi import APIRouter, HTTPException

from src.api.dependencies import CurrentUserDep
from src.schemas.contact_schema import ContactAddDTO
from src.services.contact_service import contact_service

router = APIRouter(prefix="/bank_app/v1/contacts", tags=["Contact"])


@router.post("/add")
async def add_contact(
    contact: ContactAddDTO, current_user: CurrentUserDep
) -> dict[str, bool | Any]:
    added_contact = await contact_service.create_new_contact(
        current_user.user_id, contact.phone_number
    )
    if not added_contact:
        raise HTTPException(status_code=409, detail="Contact already exists")
    return {"success": True, "contact": added_contact}


@router.get("/find")
async def find_user(phone_number: str, current_user: CurrentUserDep) -> dict[str, bool | Any]:
    found_user = await contact_service.validate_find_user_by_phone_number(phone_number)
    if not found_user:
        return {"success": False, "message": "Contact not found."}
    return {"success": True, "user": found_user}


@router.get("/all")
async def all_contacts(current_user: CurrentUserDep) -> dict[str, bool | Any]:
    contact_list = await contact_service.validate_all_contacts_from_user(current_user.user_id)
    if not contact_list:
        return {"success": False, "message": "Contact list empty."}
    return {"success": True, "contacts": contact_list}


@router.delete("/delete/{contact_id}")
async def delete_contact(
    contact_id: int, current_user: CurrentUserDep
) -> dict[str, bool | Any]:
    response = await contact_service.response_delete_contact(contact_id)
    if not response:
        raise HTTPException(status_code=404, detail="Contact not found.")
    return {"success": True}
