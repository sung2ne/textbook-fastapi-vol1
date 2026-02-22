from fastapi import APIRouter, HTTPException, status
from app.models import Todo, TodoCreate, TodoUpdate
from app import crud

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)


@router.post("", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    """할 일을 생성합니다."""
    return crud.create_todo(todo)


@router.get("", response_model=list[Todo])
def read_todos(completed: bool | None = None):
    """할 일 목록을 조회합니다."""
    return crud.get_todos(completed=completed)


@router.get(
    "/{todo_id}",
    response_model=Todo,
    responses={
        404: {
            "description": "할 일을 찾을 수 없음",
            "content": {
                "application/json": {
                    "example": {"detail": "할 일을 찾을 수 없습니다"}
                }
            }
        }
    }
)
def read_todo(todo_id: int):
    """특정 할 일을 조회합니다."""
    todo = crud.get_todo(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="할 일을 찾을 수 없습니다"
        )
    return todo


@router.patch("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate):
    """할 일을 수정합니다."""
    updated = crud.update_todo(todo_id, todo_update)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="할 일을 찾을 수 없습니다"
        )
    return updated


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    """할 일을 삭제합니다."""
    deleted = crud.delete_todo(todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="할 일을 찾을 수 없습니다"
        )
    # 204는 응답 본문이 없음
