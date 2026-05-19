from src.models.base_models import Contact
from src.repositories.contact_repository import contact_repository
from src.schemas.relationships import UserContactRelDTO
from src.schemas.contact_schema import ContactDTO

class ContactService:

    @staticmethod
    def create_new_contact(user_id: int, phone_number: str) -> list[ContactDTO] | None:
        target_contact = contact_service.validate_find_user_by_phone_number(
            phone_number
        )
        convert_model = Contact(
            user_id=user_id,
            first_name=target_contact[0].first_name,
            last_name=target_contact[0].last_name,
            super_last_name=target_contact[0].super_last_name,
            phone_number=target_contact[0].phone_number,
        )
        added_contact = contact_repository.create_contact_in_db(convert_model)
        if added_contact:
            result_dto = [
                ContactDTO.model_validate(added_contact, from_attributes=True)
            ]
            return result_dto
        return None

    @staticmethod
    def validate_find_user_by_phone_number(
        phone_number: str,
    ) -> list[ContactDTO] | None:
        found_user = contact_repository.find_user_by_phone_number(phone_number)
        if found_user:
            result_dto = [
                ContactDTO.model_validate(row, from_attributes=True)
                for row in found_user
            ]
            return result_dto
        return None

    @staticmethod
    def validate_all_contacts_from_user(user_id: int) -> list[UserContactRelDTO] | None:
        all_contacts = contact_repository.get_all_contacts_from_user(user_id)
        if all_contacts:
            result_dto = [
                UserContactRelDTO.model_validate(row, from_attributes=True)
                for row in all_contacts
            ]
            return result_dto
        return None

    @staticmethod
    def response_delete_contact(contact_id: int) -> bool:
        return contact_repository.delete_contact_in_db(contact_id)


contact_service = ContactService()
