from datetime import datetime
from sqlmodel import SQLModel, Field


class TodoBase(SQLModel):
    """공통 필드"""
    title: str = Field(min_length=1, max_length=100, description="할 일 제목")
    description: str | None = Field(default=None, max_length=500, description="상세 설명")


class TodoCreate(TodoBase):
    """할 일 생성 요청"""
    pass


class TodoUpdate(SQLModel):
    """할 일 수정 요청"""
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None


class Todo(TodoBase, table=True):
    """할 일 (데이터베이스 테이블)"""
    id: int | None = Field(default=None, primary_key=True)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "FastAPI 공부하기",
                    "description": "PART 06까지 완료하기",
                    "completed": False,
                    "created_at": "2024-01-01T10:00:00"
                }
            ]
        }
    }
