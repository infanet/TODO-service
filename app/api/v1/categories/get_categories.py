from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import CategoryResponse
from db import get_async_session
from services import CategoryService

router = APIRouter()


@router.get("/", response_model=list[CategoryResponse])
async def handle_get_categories(session: AsyncSession = Depends(get_async_session)):
    results = await CategoryService(session).get_categories()
    return results
