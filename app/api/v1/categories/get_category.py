from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import CategoriesUserResponse
from db import get_async_session
from services import CategoryService

router = APIRouter()


@router.get("/one", response_model=CategoriesUserResponse)
async def handle_get_category(
    user_id: int,
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await CategoryService(session).get_category_by_users(
        user_id=user_id, category_id=category_id
    )
