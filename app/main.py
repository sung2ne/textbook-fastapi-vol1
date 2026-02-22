from enum import Enum
from fastapi import FastAPI, Query

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

# 가상 아이템 데이터
fake_items = [
    {"id": 1, "name": "노트북", "category": "electronics", "price": 1500000},
    {"id": 2, "name": "키보드", "category": "electronics", "price": 150000},
    {"id": 3, "name": "청바지", "category": "clothing", "price": 80000},
    {"id": 4, "name": "티셔츠", "category": "clothing", "price": 30000},
    {"id": 5, "name": "사과", "category": "food", "price": 3000},
]


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
def read_items(
    skip: int = 0,
    limit: int = Query(default=10, le=100),
    q: str | None = Query(default=None, min_length=1, description="검색어"),
    category: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
):
    """
    아이템 목록을 조회합니다.

    - skip: 건너뛸 개수
    - limit: 가져올 개수 (최대 100)
    - q: 이름 검색어
    - category: 카테고리 필터
    - min_price: 최소 가격
    - max_price: 최대 가격
    """
    results = fake_items

    # 검색어 필터
    if q:
        results = [item for item in results if q in item["name"]]

    # 카테고리 필터
    if category:
        results = [item for item in results if item["category"] == category]

    # 가격 필터
    if min_price is not None:
        results = [item for item in results if item["price"] >= min_price]
    if max_price is not None:
        results = [item for item in results if item["price"] <= max_price]

    # 페이지네이션
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
