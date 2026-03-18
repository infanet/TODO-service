from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from db import get_async_session
from models import User
from schemas import TokenResponse, RefreshRequest
from services import AuthService

router = APIRouter()


@router.post("/refresh", response_model=TokenResponse)
async def handle_refresh(
    refresh_user: RefreshRequest,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await AuthService(session).refresh(refresh_user)
