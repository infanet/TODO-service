from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import TagResponse
from services import TagService

router = APIRouter()


@router.delete("/delete", response_model=TagResponse)
async def handle_delete_tag(
    tag_id: int, session: AsyncSession = Depends(get_async_session)
):
    return await TagService(session).delete_tag(tag_id)
