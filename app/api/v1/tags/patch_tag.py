from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import TagResponse, TagPatch
from services import TagService

router = APIRouter()


@router.patch("/patch", response_model=TagResponse)
async def handle_patch_tag(
    user_id: int,
    tag_id: int,
    new_tag: TagPatch,
    session: AsyncSession = Depends(get_async_session),
):
    return await TagService(session).patch_tag(
        user_id=user_id, tag_id=tag_id, new_tag=new_tag
    )
