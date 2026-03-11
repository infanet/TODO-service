from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from repositories import CategoryRepository, UserRepository
from schemas import CategoryCreate


def category_repositories(session: AsyncSession) -> CategoryRepository:
    return CategoryRepository(session)


async def get_categories(session: AsyncSession):
    categories = await category_repositories(session).get_all()
    return categories


async def create_category(user_id, session: AsyncSession, data: CategoryCreate):
    user = await UserRepository(session).get_by_one(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    result = await category_repositories(session).create(data=data, user_id=user_id)
    return result
