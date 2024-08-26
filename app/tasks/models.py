from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database import Base


class Tasks(Base): # DeclarativeBase позволяет описывать модели SQLAlchemy с помощью ORM (Object-Relational Mapping) и автоматически генерирует SQLAlchemy схему БД
    __tablename__ = 'Tasks' # имя таблицы в БД
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True) # primary_key=True указывает, что поле является первичным ключом и автоматически генерируется на основании имени. Первичный ключ - уникальное поле, которое не может повторяться в таблице. Первичный ключ является уникальным идентификатором строки в БД. autoincrement=True указывает, что поле будет автоматически генерироваться на основании внутреннего счетчика
    name: Mapped[str] # Mapped в данном случае обозначает, что поле будет соответствовать полю в БД с таким же именем
    pomodoro_count: Mapped[int]
    category_id: Mapped[int] = mapped_column(nullable=False) # nullable=False указывает, что поле должно быть обязательно заполнено
    user_id: Mapped[int] = mapped_column(ForeignKey("UserProfile.id"), nullable=False) # nullable=False


class Categories(Base): # Для описания таблицы Categories
    __tablename__ = 'Categories'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    type: Mapped[Optional[str]] # Optional[str] позволяет описать поле, которое может быть None. Альтернатива - nullable=True.
    name: Mapped[str]