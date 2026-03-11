from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import CategoryResponse
from db import get_async_session
from services import CategoryService

router = APIRouter()
