from typing import TypeVar, Type, Generic

from src.core.database import session_factory

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_by_id(self, obj_id: int) -> ModelType:
        """
        Получение модели по id
        :return: ModelType
        """
        with session_factory() as session:
            model = session.get(self.model, obj_id)
            return model
