from fastapi import Depends, HTTPException, status, Query
from app.models import Todo
from app import crud


def get_todo_or_404(todo_id: int) -> Todo:
    """
    할 일을 조회하거나 404 에러를 반환합니다.
    """
    todo = crud.get_todo(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {todo_id}인 할 일을 찾을 수 없습니다"
        )
    return todo


class PaginationParams:
    """페이지네이션 매개변수"""

    def __init__(
        self,
        skip: int = Query(default=0, ge=0, description="건너뛸 개수"),
        limit: int = Query(default=10, ge=1, le=100, description="가져올 개수")
    ):
        self.skip = skip
        self.limit = limit
