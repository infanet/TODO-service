from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from db import get_async_session
from models import User
from schemas import CommentResponse, CommentCreate
from services import CommentService

router = APIRouter()


@router.post("/create", response_model=CommentResponse)
async def handle_create_comment(
    todo_id: int,
    comment: CommentCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await CommentService(session).create_comment(
        user=current_user, todo_id=todo_id, comment=comment
    )
