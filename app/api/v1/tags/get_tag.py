from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_current_user
from db import get_async_session
from models import User
from schemas import TagItem
from services import TagService

router = APIRouter()


@router.get("/one", response_model=TagItem)
async def handle_get_tag(
    todo_id: int,
    tag_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await TagService(session).get_tag(
        todo_id=todo_id, user=current_user, tag_id=tag_id
    )
