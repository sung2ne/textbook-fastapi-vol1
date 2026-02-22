from datetime import datetime
from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    """할 일 생성 요청"""
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None


class TodoUpdate(BaseModel):
    """할 일 수정 요청"""
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None


class Todo(BaseModel):
    """할 일 응답"""
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "FastAPI 공부하기",
                    "description": "PART 05까지 완료하기",
                    "completed": False,
                    "created_at": "2024-01-01T10:00:00"
                }
            ]
        }
    }
