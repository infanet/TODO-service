from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from repositories import CategoryRepository, UserRepository
from schemas import CategoryCreate


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.category_repositories = CategoryRepository(session=session)

    async def get_categories(self):
        categories = await self.category_repositories.get_all()
        return categories

    async def create_category(self, data: CategoryCreate, user_id):
        user = await UserRepository(self.category_repositories.session).get_by_one(
            user_id
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        result = await self.category_repositories.create(data=data, user_id=user_id)
        return result
