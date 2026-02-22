from datetime import datetime
from app.models import Todo, TodoCreate, TodoUpdate
from app.database import todos_db, get_next_id


def create_todo(todo_create: TodoCreate) -> Todo:
    """할 일 생성"""
    todo = Todo(
        id=get_next_id(),
        title=todo_create.title,
        description=todo_create.description,
        completed=False,
        created_at=datetime.now()
    )
    todos_db[todo.id] = todo
    return todo


def get_todos(completed: bool | None = None) -> list[Todo]:
    """모든 할 일 조회 (필터링 가능)"""
    todos = list(todos_db.values())

    if completed is not None:
        todos = [t for t in todos if t.completed == completed]

    return todos


def get_todo(todo_id: int) -> Todo | None:
    """특정 할 일 조회"""
    return todos_db.get(todo_id)


def update_todo(todo_id: int, todo_update: TodoUpdate) -> Todo | None:
    """할 일 수정"""
    todo = todos_db.get(todo_id)
    if not todo:
        return None

    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.description is not None:
        todo.description = todo_update.description
    if todo_update.completed is not None:
        todo.completed = todo_update.completed

    return todo


def delete_todo(todo_id: int) -> Todo | None:
    """할 일 삭제"""
    return todos_db.pop(todo_id, None)
