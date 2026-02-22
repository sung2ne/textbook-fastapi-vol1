from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.database import get_session
from app.models import Token
from app.crud import user as user_crud
from app.security import create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    로그인하고 JWT 토큰을 발급받습니다.

    - **username**: 이메일
    - **password**: 비밀번호
    """
    # 사용자 인증
    user = user_crud.authenticate_user(
        session,
        email=form_data.username,  # OAuth2 스펙상 username 필드 사용
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 토큰 생성
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},  # sub에 사용자 ID 저장
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
