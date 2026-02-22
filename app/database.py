from sqlmodel import SQLModel, Session, create_engine
from app.config import DATABASE_URL

# 엔진 생성
engine = create_engine(
    DATABASE_URL,
    echo=True,  # SQL 로그 출력 (개발용)
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)


def create_db_and_tables():
    """데이터베이스와 테이블 생성"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """데이터베이스 세션 제공 (의존성)"""
    with Session(engine) as session:
        yield session
