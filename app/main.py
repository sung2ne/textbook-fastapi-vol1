from fastapi import FastAPI

app = FastAPI(
    title="나의 첫 번째 API",
    description="FastAPI로 만든 API입니다.",
    version="1.0.0"
)

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

@app.get("/users", tags=["users"])
def read_users():
    """사용자 목록 조회"""
    return {"users": []}

@app.get("/users/{user_id}", tags=["users"])
def read_user(user_id: int):
    """특정 사용자 조회"""
    return {"user_id": user_id}
