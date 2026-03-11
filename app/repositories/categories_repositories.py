from sqlalchemy import select

from models import Category
from schemas import CategoryCreate


class CategoryRepository:
    def __init__(self, session):
        self.session = session

    async def get_all(self):
        res = await self.session.execute(select(Category))
        return res.scalars().all()

    async def create(self, data: CategoryCreate, user_id):
        category = Category(**data.model_dump(), user_id=user_id)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category
