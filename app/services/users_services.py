from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from repositories import UserRepository
from core import (
    AllError,
    ErrorMessages,
)


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repositories = UserRepository(session)

    @staticmethod
    async def check_current(data_id: int, current_user_id: int):
        if data_id != current_user_id:
            raise AllError(ErrorMessages.FORBIDDEN_403).forbidden()

    async def get_users(self):
        return await self.user_repositories.get_all()

    @staticmethod
    async def get_user(user: User):
        return user

    async def delete_user(self, user: User):
        await self.user_repositories.del_user(user)
