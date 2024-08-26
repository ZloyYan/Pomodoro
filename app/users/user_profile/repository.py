from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from dataclasses import dataclass

from app.users.user_profile.models import UserProfile
from app.users.user_profile.schema import UserCreateSchema

@dataclass
class UserRepository:
    db_session: AsyncSession


    async def get_user_by_email(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def create_user(self, user: UserCreateSchema) -> UserProfile:
        query = insert(UserProfile).values(
            **user.model_dump()
        ).returning(UserProfile.id)
        async with self.db_session as session:
            user_id: int = (await session.execute(query)).scalar()
            session.commit()  # Committing the transaction to persist the user in the database
            return  await self.get_user(user_id)
    
    async def get_user(self, user_id: int) -> UserProfile | None: # UserProfile | None подсказка, которая означает, что может вернуть None или экземпляр UserProfile:
        query = select(UserProfile).where(UserProfile.id == user_id)
        async with self.db_session as session:
            user = (await session.execute(query)).scalar_one_or_none()
            return user
        
    async def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()


