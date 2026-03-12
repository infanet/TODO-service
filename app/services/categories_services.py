from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from repositories import CategoryRepository, UserRepository
from schemas import CategoryCreate


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.http_404_user = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
        self.http_404_category = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
        self.user_repositories = UserRepository(session)
        self.category_repositories = CategoryRepository(session)

    async def get_categories(self):
        categories = await self.category_repositories.get_all()
        return categories

    async def get_category_by_users(self, user_id: int, category_id: int):
        user = await self.user_repositories.get_by_one(user_id)
        if not user:
            raise self.http_404_user
        user_categories = await self.category_repositories.get_id_user_categories(
            user_id, category_id
        )
        return user_categories

    async def create_category(self, data: CategoryCreate, user_id):
        user = await self.user_repositories.get_by_one(user_id)
        if not user:
            raise self.http_404_user

        result = await self.category_repositories.create(data=data, user_id=user_id)
        return result

    async def patch_category(self, new_category, category_id):
        category = await self.category_repositories.get_by_id(category_id)
        if not category:
            raise self.http_404_category
        return await self.category_repositories.patch(category, new_category)

    async def delete_category(self, category_id: int):
        category = await self.category_repositories.get_by_id(category_id)
        if not category:
            raise self.http_404_category
        await self.category_repositories.del_category(category)
        return category
