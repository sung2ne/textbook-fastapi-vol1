from fastapi import Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session
from app.database import get_session
from app.models import User, Post, TokenData
from app.crud import post as post_crud, user as user_crud
from app.config import settings


# 토큰 URL 지정 (로그인 엔드포인트)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_post_or_404(
    post_id: int,
    session: Session = Depends(get_session)
) -> Post:
    """게시글 조회 또는 404"""
    post = post_crud.get_post(session, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )
    return post


class Pagination:
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="페이지 번호"),
        size: int = Query(default=10, ge=1, le=100, description="페이지 크기")
    ):
        self.page = page
        self.size = size
        self.skip = (page - 1) * size


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    """토큰을 검증하고 현재 사용자를 반환합니다."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보가 유효하지 않습니다",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 토큰 디코딩
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=int(user_id))

    except JWTError:
        raise credentials_exception

    # 사용자 조회
    user = user_crud.get_user(session, token_data.user_id)

    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """활성 상태인 현재 사용자를 반환합니다."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비활성화된 계정입니다"
        )
    return current_user


def get_current_user_optional(
    token: str | None = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)),
    session: Session = Depends(get_session)
) -> User | None:
    """토큰이 있으면 사용자를 반환하고, 없으면 None을 반환합니다."""
    if token is None:
        return None

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_crud.get_user(session, int(user_id))
    except JWTError:
        return None
