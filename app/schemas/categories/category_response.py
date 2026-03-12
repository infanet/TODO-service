from pydantic import ConfigDict

from .category_base import CategoryBase
from schemas import UserResponse


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CategoriesUserResponse(UserResponse):
    categories: list[CategoryResponse]


class CategoryUserResponse(UserResponse):
    categories: CategoryResponse
