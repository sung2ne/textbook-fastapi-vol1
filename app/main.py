from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import auth, users, posts, comments


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 마이그레이션으로 테이블 관리하므로 여기서는 아무것도 안 함
    yield


app = FastAPI(
    title="게시판 API",
    description="FastAPI로 만든 게시판",
    version="1.0.0",
    lifespan=lifespan
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.get("/")
def read_root():
    return {"message": "게시판 API에 오신 것을 환영합니다"}
