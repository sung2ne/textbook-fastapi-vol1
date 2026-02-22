from sqlmodel import Session, select
from app.models import Todo, TodoCreate, TodoUpdate


def create_todo(session: Session, todo_create: TodoCreate) -> Todo:
    """할 일 생성"""
    todo = Todo.model_validate(todo_create)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def get_todos(session: Session, completed: bool | None = None) -> list[Todo]:
    """모든 할 일 조회"""
    statement = select(Todo)

    if completed is not None:
        statement = statement.where(Todo.completed == completed)

    return session.exec(statement).all()


def get_todo(session: Session, todo_id: int) -> Todo | None:
    """특정 할 일 조회"""
    return session.get(Todo, todo_id)


def update_todo(session: Session, todo: Todo, todo_update: TodoUpdate) -> Todo:
    """할 일 수정"""
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def delete_todo(session: Session, todo: Todo) -> None:
    """할 일 삭제"""
    session.delete(todo)
    session.commit()
