from sqlalchemy.ext.asyncio import AsyncSession

from repositories import UserRepository
from schemas import UserCreate
from core import (
    AllError,
    ErrorMessages,
    hash_password,
)


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repositories = UserRepository(session)

    async def get_404_not_found(self, user_id: int):
        user = await self.user_repositories.get_by_id(user_id)
        if not user:
            raise AllError(ErrorMessages.USER_404).not_found()
        return user

    async def get_users(self):
        return await self.user_repositories.get_all()

    async def get_user(self, user_id: int):
        return await self.get_404_not_found(user_id)

    async def create_user(self, user: UserCreate):
        existing_user = await self.user_repositories.get_by_email(str(user.email))
        if existing_user:
            raise AllError(ErrorMessages.USER_400).bad_request()
        hashed_password = hash_password(user.password)
        return await self.user_repositories.create(
            user=user, hashed_password=hashed_password
        )

    async def delete_user(self, user_id: int):
        user = await self.get_404_not_found(user_id)
        await self.user_repositories.del_user(user)
        return user
