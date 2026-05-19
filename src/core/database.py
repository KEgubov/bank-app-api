from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.configs.db_url_config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,
    future=True,
)

async_session = async_sessionmaker(async_engine)
