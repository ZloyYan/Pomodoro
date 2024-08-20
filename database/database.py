from typing import Any
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    id: any

    __name__: str

    __allow_unmapped__ = True # __allow_unmapped__ позволяет описывать поля,

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower() # имя таблицы в БД будет именем модели, приведенным к нижнему регистру

