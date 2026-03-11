from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import UserResponse
from services import delete_user
from repositories import UserRepository

router = APIRouter()


@router.delete("/delete")
async def handle_delete_user(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    return await delete_user(user_id=user_id, session=session)
