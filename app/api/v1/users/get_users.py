from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from services import get_users
from repositories import UserRepository
from schemas import UserResponse

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
async def handle_get_users(session: AsyncSession = Depends(get_async_session)):
    users = await get_users(UserRepository(session=session))
    return users
