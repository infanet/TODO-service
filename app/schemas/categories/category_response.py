from pydantic import ConfigDict
from .category_base import CategoryBase


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
