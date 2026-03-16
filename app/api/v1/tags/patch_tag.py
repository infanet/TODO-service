from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from db import get_async_session
from models import User
from schemas import TagResponse, TagPatch
from services import TagService

router = APIRouter()


@router.patch("/patch", response_model=TagResponse)
async def handle_patch_tag(
    user_id: int,
    tag_id: int,
    new_tag: TagPatch,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await TagService(session).patch_tag(
        user_id=user_id, tag_id=tag_id, new_tag=new_tag
    )
