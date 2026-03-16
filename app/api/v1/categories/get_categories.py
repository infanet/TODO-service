from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from models import User
from schemas import CategoryResponse
from db import get_async_session
from services import CategoryService

router = APIRouter()


@router.get("/", response_model=list[CategoryResponse])
async def handle_get_categories(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    results = await CategoryService(session).get_categories()
    return results
