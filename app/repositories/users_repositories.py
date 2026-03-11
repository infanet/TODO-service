from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import User
from schemas import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get_by_one(self, user_id: int):
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str):
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, data: UserCreate):
        new_user = User(
            username=data.username,
            email=data.email,
            hashed_password=data.password,
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def del_user(self, user):
        await self.session.delete(user)
        await self.session.commit()
