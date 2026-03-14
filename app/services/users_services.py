from sqlalchemy.ext.asyncio import AsyncSession

from repositories import UserRepository
from schemas import UserCreate
from core import AllError, ErrorMessages


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repositories = UserRepository(session)

    async def get_users(self):
        return await self.user_repositories.get_all()

    async def get_user(self, user_id: int):
        result = await self.user_repositories.get_by_id(user_id)
        if not result:
            raise AllError(ErrorMessages.USER_404).not_found()
        return result

    async def create_user(self, data: UserCreate):
        existing_user = await self.user_repositories.get_by_email(str(data.email))
        if existing_user:
            raise AllError(ErrorMessages.USER_400).bad_request()
        return await self.user_repositories.create(data)

    async def delete_user(self, user_id: int):
        user = await self.user_repositories.get_by_id(user_id)
        if not user:
            raise AllError(ErrorMessages.USER_404).not_found()
        await self.user_repositories.del_user(user)
        return user
