from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """페이지네이션 응답"""
    items: list[T]
    total: int
    page: int
    size: int
    pages: int  # 전체 페이지 수
