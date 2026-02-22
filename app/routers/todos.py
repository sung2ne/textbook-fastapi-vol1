from fastapi import APIRouter, status
from app.models import Todo, TodoCreate, TodoUpdate
from app import crud

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)


@router.post("", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    """
    할 일을 생성합니다.

    - **title**: 할 일 제목 (필수, 1~100자)
    - **description**: 상세 설명 (선택)
    """
    return crud.create_todo(todo)


@router.get("", response_model=list[Todo])
def read_todos(completed: bool | None = None):
    """
    할 일 목록을 조회합니다.

    - **completed**: True(완료), False(미완료), None(전체)
    """
    return crud.get_todos(completed=completed)


@router.get("/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    """
    특정 할 일을 조회합니다.
    """
    todo = crud.get_todo(todo_id)
    if not todo:
        return {"error": "할 일을 찾을 수 없습니다"}
    return todo


@router.patch("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoUpdate):
    """
    할 일을 수정합니다.

    수정할 필드만 전달하면 됩니다.
    """
    updated = crud.update_todo(todo_id, todo)
    if not updated:
        return {"error": "할 일을 찾을 수 없습니다"}
    return updated


@router.delete("/{todo_id}")
def delete_todo(todo_id: int):
    """
    할 일을 삭제합니다.
    """
    deleted = crud.delete_todo(todo_id)
    if not deleted:
        return {"error": "할 일을 찾을 수 없습니다"}
    return {"message": "삭제되었습니다", "deleted": deleted}
