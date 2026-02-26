from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PageInfo(BaseModel):
    total_results: int
    results_per_page: int


class ListResponse(BaseModel, Generic[T]):
    kind: str
    items: list[T]
    page_info: PageInfo | None = None


class ItemResponse(BaseModel, Generic[T]):
    kind: str
    item: T
