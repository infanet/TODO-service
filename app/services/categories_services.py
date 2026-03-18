from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from repositories import CategoryRepository
from services import UserService
from schemas import CategoryCreate, CategoryPatch
from core import AllError, ErrorMessages


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.user_services = UserService(session)
        self.category_repositories = CategoryRepository(session)

    async def get_404_not_found(self, category_id: int):
        category = await self.category_repositories.get_by_id(category_id)
        if not category:
            raise AllError(ErrorMessages.CATEGORY_404).not_found()
        return category

    async def get_categories(self, current_user: User):
        return await self.category_repositories.get_all(current_user)

    async def get_category_by_user(self, user: User, category_id: int):
        category = await self.get_404_not_found(category_id)
        await self.user_services.check_current(
            data_id=category.user_id, current_user_id=user.id
        )
        return await self.category_repositories.get_id_user_category(
            user_id=user.id, category_id=category_id
        )

    async def create_category(self, category: CategoryCreate, user: User):
        return await self.category_repositories.create(category=category, user=user)

    async def patch_category(
        self, new_category: CategoryPatch, category_id: int, current_user: User
    ):
        category = await self.get_404_not_found(category_id)
        await self.user_services.check_current(
            data_id=category.user_id, current_user_id=current_user.id
        )
        return await self.category_repositories.patch(category, new_category)

    async def delete_category(self, category_id: int, current_user: User):
        category = await self.get_404_not_found(category_id)
        await self.user_services.check_current(
            data_id=category.user_id, current_user_id=current_user.id
        )
        await self.category_repositories.del_category(category)
        return category
