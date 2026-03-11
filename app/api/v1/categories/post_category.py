from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import CategoryResponse, CategoryCreate
from db import get_async_session
from services import create_category

router = APIRouter()


@router.post(
    "/create", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED
)
async def handle_create_category(
    user_id: int,
    data: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
):
    result = await create_category(session=session, user_id=user_id, data=data)
    return result
