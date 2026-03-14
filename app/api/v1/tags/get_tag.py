from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import TagItem
from services import TagService

router = APIRouter()


@router.get("/one", response_model=TagItem)
async def handle_get_tag(
    user_id: int, tag_id: int, session: AsyncSession = Depends(get_async_session)
):
    return await TagService(session).get_tag(user_id=user_id, tag_id=tag_id)
