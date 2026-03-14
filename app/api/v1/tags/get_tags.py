from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import TagResponse
from db import get_async_session
from services import TagService

router = APIRouter()


@router.get("/all", response_model=list[TagResponse])
async def handle_get_tags(session: AsyncSession = Depends(get_async_session)):
    return await TagService(session).get_tags()
