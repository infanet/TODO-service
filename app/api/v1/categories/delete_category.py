from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import CategoryResponse, CategoriesUserResponse
from db import get_async_session
from services import CategoryService

router = APIRouter()


@router.delete("/delete", response_model=CategoryResponse)
async def handle_delete_category(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    return await CategoryService(session).delete_category(category_id)
