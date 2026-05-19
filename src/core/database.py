from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.configs.db_url_config import settings

engine = create_engine(
    url=settings.DATABASE_URL,
    echo=True,
    future=True,
)

session_factory = sessionmaker(bind=engine)
