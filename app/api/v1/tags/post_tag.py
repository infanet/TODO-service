from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from db import get_async_session
from models import User
from schemas import TagResponse, TagCreate
from services import TagService

router = APIRouter()


@router.post("/create", response_model=TagResponse)
async def handle_create_tag(
    todo_id: int,
    tag: TagCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await TagService(session).create_tag(
        todo_id=todo_id, user=current_user, tag=tag
    )
