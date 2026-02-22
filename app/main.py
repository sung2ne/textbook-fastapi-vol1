from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.logging_config import setup_logging
from app.middleware import log_requests
from app.routers import auth, users, posts, comments
from app.config import settings

# 로깅 설정
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("애플리케이션 시작")
    yield
    logger.info("애플리케이션 종료")


app = FastAPI(
    title="게시판 API",
    description="FastAPI로 만든 게시판",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 요청 로깅 미들웨어
app.middleware("http")(log_requests)

# 라우터 등록
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.get("/")
def read_root():
    return {"message": "게시판 API에 오신 것을 환영합니다"}
