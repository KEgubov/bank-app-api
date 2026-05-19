from src.models.base_models import User
from src.repositories.user_repository import user_repository
from src.schemas.custom import FirstLastSuperNameDTO, CurrentUserDTO
from src.schemas.user_schema import UserDTO, UserAddDTO
from src.services.decorator import validate_phone_number

class UserService:

    @staticmethod
    def validate_user(user: UserAddDTO) -> list[UserDTO] | None:
        model_user = User(**user.model_dump())
        added_user = user_repository.create_user_in_db(model_user)
        if added_user:
            result_dto = [UserDTO.model_validate(added_user, from_attributes=True)]
            return result_dto
        return None

    @staticmethod
    def validate_current_user(user_id: int) -> CurrentUserDTO | None:
        model_user = user_repository.get_current_user_in_db(user_id=user_id)
        if model_user:
            result_dto = CurrentUserDTO.model_validate(model_user, from_attributes=True)
            return result_dto
        return None

    @staticmethod
    @validate_phone_number()
    def validate_target_name(phone_number: str) -> list[FirstLastSuperNameDTO] | None:
        target_name = user_repository.get_target_name(phone_number)
        if target_name:
            result_dto = [
                FirstLastSuperNameDTO.model_validate(row, from_attributes=True)
                for row in target_name
            ]
            return result_dto
        return None

    @staticmethod
    def validate_user_profile(user_id: int) -> list[UserDTO] | None:
        model_user = user_repository.get_user_profile(user_id=user_id)
        if model_user:
            result_dto = [
                UserDTO.model_validate(row, from_attributes=True) for row in model_user
            ]
            return result_dto
        return None

    @staticmethod
    def validate_owner_name(user_id: int) -> list[FirstLastSuperNameDTO] | None:
        model_owner = user_repository.get_find_owner_name(user_id)
        if model_owner:
            result_dto = [
                FirstLastSuperNameDTO.model_validate(row, from_attributes=True)
                for row in model_owner
            ]
            return result_dto
        return None


user_service = UserService()
