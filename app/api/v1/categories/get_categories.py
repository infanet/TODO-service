from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import CategoryResponse
from db import get_async_session
from services import get_categories

router = APIRouter()


@router.get("/", response_model=list[CategoryResponse])
async def handle_get_categories(session: AsyncSession = Depends(get_async_session)):
    results = await get_categories(session)
    return results
