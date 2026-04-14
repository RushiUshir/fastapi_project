from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_previous: bool
    has_next: bool


class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    meta: PaginationMeta

