from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.models import Todo, TodoCreate, TodoUpdate
from app import crud
from app.database import get_session
from app.dependencies import get_todo_or_404, PaginationParams

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    session: Session = Depends(get_session)
):
    """
    할 일을 생성합니다.

    - **title**: 할 일 제목 (필수, 1~100자)
    - **description**: 상세 설명 (선택)
    """
    return crud.create_todo(session, todo)


@router.get("", response_model=list[Todo])
def read_todos(
    session: Session = Depends(get_session),
    completed: bool | None = None,
    pagination: PaginationParams = Depends()
):
    """
    할 일 목록을 조회합니다.

    - **completed**: True(완료), False(미완료), None(전체)
    """
    todos = crud.get_todos(session, completed=completed)
    return todos[pagination.skip:pagination.skip + pagination.limit]


@router.get("/{todo_id}", response_model=Todo)
def read_todo(todo: Todo = Depends(get_todo_or_404)):
    """특정 할 일을 조회합니다."""
    return todo


@router.patch("/{todo_id}", response_model=Todo)
def update_todo(
    todo_update: TodoUpdate,
    todo: Todo = Depends(get_todo_or_404),
    session: Session = Depends(get_session)
):
    """
    할 일을 수정합니다.

    수정할 필드만 전달하면 됩니다.
    """
    return crud.update_todo(session, todo, todo_update)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo: Todo = Depends(get_todo_or_404),
    session: Session = Depends(get_session)
):
    """할 일을 삭제합니다."""
    crud.delete_todo(session, todo)
