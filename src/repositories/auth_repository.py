from sqlalchemy import select, and_, Row

from src.core.database import async_session
from src.models.base_models import User
from src.repositories.base_repository import BaseRepository
from src.schemas.custom import LoginData


class Authenticate(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    @staticmethod
    async def authenticate_user(creds: LoginData) -> Row[tuple[int, str]]:
        async with async_session() as session:
            query = (
                select(User.user_id)
                .where(User.phone_number == creds.phone_number,
                       and_(User.password == creds.password))
            )
            result = await session.execute(query)
            return result.first() if result else None


auth = Authenticate()
