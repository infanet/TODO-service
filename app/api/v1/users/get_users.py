from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from services import get_users
from repositories import UserRepository

router = APIRouter()


@router.get("/")
async def get_user(session: AsyncSession = Depends(get_async_session)):
    users = await get_users(UserRepository(session=session))
    return users
