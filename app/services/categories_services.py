from sqlalchemy.ext.asyncio import AsyncSession

from repositories import CategoryRepository, UserRepository
from schemas import CategoryCreate
from core import AllError, ErrorMessages


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.user_repositories = UserRepository(session)
        self.category_repositories = CategoryRepository(session)

    async def get_categories(self):
        return await self.category_repositories.get_all()

    async def get_category_by_users(self, user_id: int, category_id: int):
        user = await self.user_repositories.get_by_id(user_id)
        if not user:
            raise AllError(ErrorMessages.USER_404).not_found()
        return await self.category_repositories.get_id_user_categories(
            user_id, category_id
        )

    async def create_category(self, data: CategoryCreate, user_id):
        user = await self.user_repositories.get_by_id(user_id)
        if not user:
            raise AllError(ErrorMessages.USER_404).not_found()

        return await self.category_repositories.create(data=data, user_id=user_id)

    async def patch_category(self, new_category, category_id):
        category = await self.category_repositories.get_by_id(category_id)
        if not category:
            raise AllError(ErrorMessages.CATEGORY_404).not_found()
        return await self.category_repositories.patch(category, new_category)

    async def delete_category(self, category_id: int):
        category = await self.category_repositories.get_by_id(category_id)
        if not category:
            raise AllError(ErrorMessages.CATEGORY_404).not_found()
        await self.category_repositories.del_category(category)
        return category
