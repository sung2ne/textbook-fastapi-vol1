from fastapi import FastAPI
from app.routers import todos

app = FastAPI(
    title="TODO API",
    description="할 일 관리 API",
    version="1.0.0"
)

# 라우터 등록
app.include_router(todos.router)

@app.get("/")
def read_root():
    return {"message": "TODO API에 오신 것을 환영합니다"}
