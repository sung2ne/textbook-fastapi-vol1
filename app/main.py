from datetime import datetime
from enum import Enum
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI(
    title="나의 첫 번째 API",
    description="FastAPI로 만든 API입니다.",
    version="1.0.0"
)

# ---- 가상 데이터베이스 ----

fake_users_db = {
    1: {"id": 1, "name": "홍길동", "email": "hong@example.com"},
    2: {"id": 2, "name": "김철수", "email": "kim@example.com"},
    3: {"id": 3, "name": "이영희", "email": "lee@example.com"},
}

fake_items = [
    {"id": 1, "name": "노트북", "category": "electronics", "price": 1500000},
    {"id": 2, "name": "키보드", "category": "electronics", "price": 150000},
    {"id": 3, "name": "청바지", "category": "clothing", "price": 80000},
    {"id": 4, "name": "티셔츠", "category": "clothing", "price": 30000},
    {"id": 5, "name": "사과", "category": "food", "price": 3000},
]

todos_db: dict[int, "Todo"] = {}
todo_id_counter = 1


# ---- Pydantic 모델 ----

class ItemCategory(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"


class UserCreate(BaseModel):
    name: str
    age: int
    email: str


class TodoCreate(BaseModel):
    """할 일 생성 요청"""
    title: str = Field(min_length=1, max_length=100, examples=["FastAPI 공부하기"])
    description: str | None = Field(default=None, max_length=500)


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None


class Todo(BaseModel):
    """할 일 응답"""
    id: int
    title: str
    description: str | None
    completed: bool = False
    created_at: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "FastAPI 공부하기",
                    "description": "PART 04까지 완료하기",
                    "completed": False,
                    "created_at": "2024-01-01T10:00:00"
                }
            ]
        }
    }


# ---- API 엔드포인트 ----

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/hello")
def say_hello():
    return {"greeting": "안녕하세요!"}

@app.get(
    "/items",
    summary="아이템 목록 조회",
    description="저장된 모든 아이템의 목록을 반환합니다.",
    tags=["items"]
)
def read_items(
    skip: int = 0,
    limit: int = Query(default=10, le=100),
    q: str | None = Query(default=None, min_length=1, description="검색어"),
    category: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
):
    results = fake_items

    if q:
        results = [item for item in results if q in item["name"]]
    if category:
        results = [item for item in results if item["category"] == category]
    if min_price is not None:
        results = [item for item in results if item["price"] >= min_price]
    if max_price is not None:
        results = [item for item in results if item["price"] <= max_price]

    return {
        "total": len(results),
        "items": results[skip:skip + limit]
    }

@app.get("/items/{category}", tags=["items"])
def read_items_by_category(category: ItemCategory):
    return {"category": category, "message": f"{category.value} 카테고리 아이템"}

@app.get("/search", tags=["items"])
def search_items(q: str | None = None):
    if q:
        return {"query": q, "results": [f"{q} 검색 결과"]}
    return {"query": None, "results": []}

@app.get("/files/{file_path:path}", tags=["files"])
def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/users", tags=["users"])
def read_users():
    """사용자 목록 조회"""
    return {"users": []}

@app.get("/users/me", tags=["users"])
def read_current_user():
    return {"user": "현재 사용자"}

@app.post("/users", tags=["users"])
def create_user(user: UserCreate):
    return {"message": f"{user.name}님이 등록되었습니다", "user": user}

@app.put("/users/{user_id}", tags=["users"])
def update_user(user_id: int, user: UserCreate):
    return {
        "user_id": user_id,
        "updated_user": user
    }

@app.get("/users/{user_id}", tags=["users"])
def read_user(user_id: int):
    """특정 사용자 조회"""
    if user_id in fake_users_db:
        return fake_users_db[user_id]
    return {"error": "사용자를 찾을 수 없습니다"}

@app.get("/users/{user_id}/items", tags=["users"])
def read_user_items(user_id: int, skip: int = 0, limit: int = 10):
    return {
        "user_id": user_id,
        "skip": skip,
        "limit": limit
    }

@app.get("/users/{user_id}/posts/{post_id}", tags=["users"])
def read_user_post(user_id: int, post_id: int):
    return {
        "user_id": user_id,
        "post_id": post_id
    }

# TODO CRUD

@app.post("/todos", response_model=Todo, tags=["todos"])
def create_todo(todo: TodoCreate):
    """할 일 생성"""
    global todo_id_counter

    new_todo = Todo(
        id=todo_id_counter,
        title=todo.title,
        description=todo.description,
        completed=False,
        created_at=datetime.now()
    )
    todos_db[todo_id_counter] = new_todo
    todo_id_counter += 1

    return new_todo

@app.get("/todos", tags=["todos"])
def read_todos():
    """할 일 목록 조회"""
    return list(todos_db.values())

@app.get("/todos/{todo_id}", tags=["todos"])
def read_todo(todo_id: int):
    """특정 할 일 조회"""
    if todo_id not in todos_db:
        return {"error": "할 일을 찾을 수 없습니다"}
    return todos_db[todo_id]

@app.put("/todos/{todo_id}", tags=["todos"])
def update_todo(todo_id: int, todo: TodoUpdate):
    """할 일 수정"""
    if todo_id not in todos_db:
        return {"error": "할 일을 찾을 수 없습니다"}

    stored_todo = todos_db[todo_id]

    if todo.title is not None:
        stored_todo.title = todo.title
    if todo.description is not None:
        stored_todo.description = todo.description
    if todo.completed is not None:
        stored_todo.completed = todo.completed

    return stored_todo

@app.delete("/todos/{todo_id}", tags=["todos"])
def delete_todo(todo_id: int):
    """할 일 삭제"""
    if todo_id not in todos_db:
        return {"error": "할 일을 찾을 수 없습니다"}

    deleted = todos_db.pop(todo_id)
    return {"message": "삭제되었습니다", "deleted": deleted}
