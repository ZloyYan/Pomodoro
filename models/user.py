from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UserProfile(Base):
    __tablename__ = "UserProfile"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    google_access_token: Mapped[Optional[str]] 
    yandex_access_token: Mapped[Optional[str]] 
    email: Mapped[Optional[str]] 
    name: Mapped[Optional[str]] 