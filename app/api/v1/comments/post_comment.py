from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from schemas import CommentResponse, CommentCreate
from services import CommentService

router = APIRouter()


@router.post("/create", response_model=CommentResponse)
async def handle_create_comment(
    user_id: int,
    todo_id: int,
    comment: CommentCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await CommentService(session).create_comment(
        user_id=user_id, todo_id=todo_id, comment=comment
    )
