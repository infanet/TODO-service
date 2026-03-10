from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import UserCreate, UserResponse
from services import create_user
from repositories import UserRepository

router = APIRouter()


@router.post("/create", response_model=UserResponse)
async def handle_create_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    result = await create_user(UserRepository(session=session), user)
    return result
