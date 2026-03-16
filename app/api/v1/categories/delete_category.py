from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas import CategoryResponse
from db import get_async_session
from services import CategoryService
from ..dependencies import get_current_user

router = APIRouter()


@router.delete("/delete", response_model=CategoryResponse)
async def handle_delete_category(
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await CategoryService(session).delete_category(category_id)
