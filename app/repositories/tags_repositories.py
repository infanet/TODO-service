from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, with_loader_criteria

from models import Tag, User
from schemas import TagCreate


class TagRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        return (await self.session.scalars(select(Tag))).all()

    async def get_by_id(self, tag_id: int):
        return (
            await self.session.execute(select(Tag).where(Tag.id == tag_id))
        ).scalar_one_or_none()

    async def get_tag_user(self, user_id: int, tag_id: int):
        return (
            await self.session.execute(
                select(User)
                .options(
                    selectinload(User.tags), with_loader_criteria(Tag, Tag.id == tag_id)
                )
                .where(User.id == user_id)
            )
        ).scalar_one_or_none()

    async def create(self, user_id: int, tag: TagCreate):
        new_tag = Tag(**tag.model_dump(), user_id=user_id)
        self.session.add(new_tag)
        await self.session.commit()
        await self.session.refresh(new_tag)
        return new_tag

    async def patch(self, new_tag, tag):
        update_data = new_tag.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(tag, key, value)

        await self.session.commit()
        await self.session.refresh(tag)
        return tag

    async def del_tag(self, tag):
        await self.session.delete(tag)
        await self.session.commit()
