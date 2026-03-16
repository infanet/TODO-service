from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import RefreshRequest
from services import AuthService

router = APIRouter()


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def handle_logout(
    logout_user: RefreshRequest, session: AsyncSession = Depends(get_async_session)
):
    await AuthService(session).logout(logout_user)
