from enum import Enum
from fastapi import FastAPI

app = FastAPI(
    title="나의 첫 번째 API",
    description="FastAPI로 만든 API입니다.",
    version="1.0.0"
)

# 가상의 데이터베이스
fake_users_db = {
    1: {"id": 1, "name": "홍길동", "email": "hong@example.com"},
    2: {"id": 2, "name": "김철수", "email": "kim@example.com"},
    3: {"id": 3, "name": "이영희", "email": "lee@example.com"},
}


class ItemCategory(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"


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
def read_items():
    """
    모든 아이템 목록을 반환합니다.

    - 인증 필요 없음
    - 최대 100개까지 반환
    """
    return {"items": ["사과", "바나나", "오렌지"]}

@app.get("/items/{category}", tags=["items"])
def read_items_by_category(category: ItemCategory):
    return {"category": category, "message": f"{category.value} 카테고리 아이템"}

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

@app.get("/users/{user_id}", tags=["users"])
def read_user(user_id: int):
    """특정 사용자 조회"""
    if user_id in fake_users_db:
        return fake_users_db[user_id]
    return {"error": "사용자를 찾을 수 없습니다"}

@app.get("/users/{user_id}/posts/{post_id}", tags=["users"])
def read_user_post(user_id: int, post_id: int):
    return {
        "user_id": user_id,
        "post_id": post_id
    }
