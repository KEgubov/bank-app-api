from sqlalchemy import select, and_, Row

from src.core.database import session_factory
from src.models.base_models import User
from src.repositories.base_repository import BaseRepository
from src.schemas.custom import LoginData


class Authenticate(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    @staticmethod
    def authenticate_user(creds: LoginData) -> Row[tuple[int, str]]:
        with session_factory() as session:
            query = (
                select(User.user_id)
                .where(User.phone_number == creds.phone_number,
                       and_(User.password == creds.password))
            )
            result = session.execute(query).first()
            return result if result else None


auth = Authenticate()
