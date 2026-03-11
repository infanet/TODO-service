from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import UserResponse
from services import UserService

router = APIRouter()


@router.get("/one", response_model=UserResponse)
async def handle_get_user(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    result = await UserService(session).get_user(user_id)
    return result
