from src.core.database import engine
from models.base_models import Base

def create_tables() -> None:
    """
    Функция создаёт таблицы в базе данных
    :return: None
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

create_tables()