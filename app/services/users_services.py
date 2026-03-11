from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import UserRepository
from schemas import UserCreate


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repositories = UserRepository(session=session)

    async def get_users(self):
        users = await self.user_repositories.get_all()
        return users

    async def get_user(self, user_id: int):
        result = await self.user_repositories.get_by_one(user_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return result

    async def create_user(self, data: UserCreate):
        existing_user = await self.user_repositories.get_by_email(str(data.email))
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )
        return await self.user_repositories.create(data)

    async def delete_user(self, user_id: int):
        user = await self.user_repositories.get_by_one(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        await self.user_repositories.del_user(user)
        return user
