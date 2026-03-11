from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import UserRepository
from schemas import UserCreate


def user_repositories(session: AsyncSession) -> UserRepository:
    return UserRepository(session=session)


async def get_users(session: AsyncSession):
    users = await user_repositories(session).get_all()
    return users


async def get_user(user_id: int, session: AsyncSession):
    result = await user_repositories(session).get_by_one(user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return result


async def create_user(session: AsyncSession, data: UserCreate):
    existing_user = await user_repositories(session).get_by_email(str(data.email))
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    return await user_repositories(session).create(data)


async def delete_user(user_id: int, session: AsyncSession):
    user = await user_repositories(session).get_by_one(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return await user_repositories(session).del_user(user)
