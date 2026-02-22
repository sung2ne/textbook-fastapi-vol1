import logging
import sys
from logging.handlers import RotatingFileHandler
from app.config import settings


def setup_logging():
    """로깅 설정"""

    format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    handlers = [
        logging.StreamHandler(sys.stdout),
    ]

    # 운영 환경에서는 파일에도 저장
    if not settings.DEBUG:
        file_handler = RotatingFileHandler(
            "app.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(format_string))
        handlers.append(file_handler)

    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format=format_string,
        handlers=handlers
    )

    # SQLAlchemy 로그는 WARNING 이상만
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    # uvicorn 로그 설정
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
