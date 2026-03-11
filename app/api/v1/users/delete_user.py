from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from services import UserService

router = APIRouter()


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def handle_delete_user(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    await UserService(session).delete_user(user_id)
