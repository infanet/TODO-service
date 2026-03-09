from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_async_session
from app.models import User

router = APIRouter()


@router.get("/")
async def get_user(session: AsyncSession = Depends(get_async_session)):
    stmt = await session.execute(select(User))
    return stmt.scalars().all()
