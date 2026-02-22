from fastapi import APIRouter, Depends, status
from app.models import Todo, TodoCreate, TodoUpdate
from app import crud
from app.dependencies import get_todo_or_404, PaginationParams

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    """할 일을 생성합니다."""
    return crud.create_todo(todo)


@router.get("", response_model=list[Todo])
def read_todos(
    completed: bool | None = None,
    pagination: PaginationParams = Depends()
):
    """할 일 목록을 조회합니다."""
    todos = crud.get_todos(completed=completed)
    return todos[pagination.skip:pagination.skip + pagination.limit]


@router.get("/{todo_id}", response_model=Todo)
def read_todo(todo: Todo = Depends(get_todo_or_404)):
    """특정 할 일을 조회합니다."""
    return todo


@router.patch("/{todo_id}", response_model=Todo)
def update_todo(
    todo_update: TodoUpdate,
    todo: Todo = Depends(get_todo_or_404)
):
    """할 일을 수정합니다."""
    return crud.update_todo(todo.id, todo_update)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo: Todo = Depends(get_todo_or_404)):
    """할 일을 삭제합니다."""
    crud.delete_todo(todo.id)
