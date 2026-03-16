from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from models import User
from schemas import CategoryPatch, CategoryResponse
from db import get_async_session
from services import CategoryService

router = APIRouter()


@router.patch("/patch", response_model=CategoryResponse)
async def handle_patch_category(
    category_id: int,
    new_category: CategoryPatch,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await CategoryService(session).patch_category(
        new_category=new_category,
        category_id=category_id,
    )
