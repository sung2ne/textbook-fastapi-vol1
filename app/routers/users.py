from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_session
from app.models import User, UserCreate, UserResponse
from app.crud import user as user_crud

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    """
    새 사용자를 생성합니다.

    - **email**: 이메일 (유니크)
    - **username**: 사용자명
    - **password**: 비밀번호 (8자 이상)
    """
    # 이메일 중복 확인
    existing_user = user_crud.get_user_by_email(session, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다"
        )

    return user_crud.create_user(session, user)


@router.get("", response_model=list[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    """사용자 목록을 조회합니다."""
    return user_crud.get_users(session, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, session: Session = Depends(get_session)):
    """특정 사용자를 조회합니다."""
    user = user_crud.get_user(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    return user
