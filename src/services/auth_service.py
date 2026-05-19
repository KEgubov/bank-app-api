from src.repositories.auth_repository import auth
from src.schemas.custom import LoginData, UserIDDTO


class AuthService:

    @staticmethod
    def resp_authenticate_user(creds: LoginData) -> UserIDDTO | None:
        resp = auth.authenticate_user(creds)
        if resp:
            result_dto = UserIDDTO.model_validate(resp, from_attributes=True)
            return result_dto
        return None


auth_service = AuthService()
