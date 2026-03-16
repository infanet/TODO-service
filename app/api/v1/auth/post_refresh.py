from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import TokenResponse, RefreshRequest
from services import AuthService

router = APIRouter()


@router.post("/refresh", response_model=TokenResponse)
async def handle_refresh(
    refresh_user: RefreshRequest, session: AsyncSession = Depends(get_async_session)
):
    return await AuthService(session).refresh(refresh_user)
