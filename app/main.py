from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import create_db_and_tables
from app.routers import todos


@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 시작/종료 시 실행되는 코드"""
    # 시작 시: 테이블 생성
    create_db_and_tables()
    yield
    # 종료 시: (필요하면 정리 코드)


app = FastAPI(
    title="TODO API",
    description="할 일 관리 API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(todos.router)


@app.get("/")
def read_root():
    return {"message": "TODO API에 오신 것을 환영합니다"}


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
