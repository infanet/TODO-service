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
