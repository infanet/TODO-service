from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from db import get_async_session
from models import User
from schemas import TagResponse
from services import TagService

router = APIRouter()


@router.delete("/delete", response_model=TagResponse)
async def handle_delete_tag(
    tag_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await TagService(session).delete_tag(tag_id=tag_id, user=current_user)
