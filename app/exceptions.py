from fastapi import HTTPException, status


class TodoNotFoundError(HTTPException):
    def __init__(self, todo_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ID {todo_id}인 할 일을 찾을 수 없습니다"
        )


class DuplicateTitleError(HTTPException):
    def __init__(self, title: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"'{title}' 제목의 할 일이 이미 존재합니다"
        )
