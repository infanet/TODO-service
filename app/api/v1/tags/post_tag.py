from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import TagResponse, TagCreate
from services import TagService

router = APIRouter()


@router.post("/create", response_model=TagResponse)
async def handle_create_tag(
    user_id: int, tag: TagCreate, session: AsyncSession = Depends(get_async_session)
):
    return await TagService(session).create_tag(user_id=user_id, tag=tag)
