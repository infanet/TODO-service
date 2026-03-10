from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db import get_async_session
from models import User

router = APIRouter()


@router.post("/create")
async def create_user(
    user,
    session: AsyncSession = Depends(get_async_session),
):
    new_user = User(**user)
    session.add(new_user)
    await session.commit()
    return new_user
