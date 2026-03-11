from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import UserResponse
from repositories import UserRepository
from services import get_user

router = APIRouter()


@router.get("/one", response_model=UserResponse)
async def handle_get_user(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    result = await get_user(user_id=user_id, session=session)
    return result
