from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 기본값이 있으면 환경 변수가 없어도 됨
    DATABASE_URL: str = "sqlite:///./board.db"
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 환경별 설정
    DEBUG: bool = False
    ALLOWED_HOSTS: list[str] = ["*"]

    # CORS 설정
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # React 개발 서버
        "http://localhost:5173",  # Vite 개발 서버
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    class Config:
        env_file = ".env"  # .env 파일에서 읽기
        env_file_encoding = "utf-8"


settings = Settings()
