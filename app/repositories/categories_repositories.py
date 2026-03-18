from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, with_loader_criteria

from models import Category, User
from schemas import CategoryCreate


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, current_user: User):
        return (
            await self.session.execute(
                select(User)
                .options(selectinload(User.categories))
                .where(User.id == current_user.id)
            )
        ).scalar_one()

    async def get_by_id(self, category_id):
        category = await self.session.execute(
            select(Category).where(Category.id == category_id)
        )
        return category.scalar_one_or_none()

    async def get_id_user_category(self, user_id: int, category_id: int):
        user_categories = await self.session.execute(
            select(User)
            .options(
                selectinload(User.categories),
                with_loader_criteria(Category, Category.id == category_id),
            )
            .where(User.id == user_id)
        )
        return user_categories.scalar_one()

    async def create(self, category: CategoryCreate, user: User):
        category = Category(**category.model_dump(), user_id=user.id)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def patch(
        self,
        category,
        new_category,
    ):
        update_data = new_category.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(category, key, value)

        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def del_category(self, category):
        await self.session.delete(category)
        await self.session.commit()
