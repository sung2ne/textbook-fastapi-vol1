from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session
from app.database import get_session
from app.models import Post, PostCreate, PostUpdate, PostResponse, PostListResponse
from app.crud import post as post_crud
from app.dependencies import Pagination

router = APIRouter(prefix="/posts", tags=["posts"])


# 임시: 로그인한 사용자 ID (다음 파트에서 실제 인증으로 교체)
def get_current_user_id() -> int:
    return 1  # 임시로 사용자 ID 1을 반환


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    게시글을 작성합니다.

    - **title**: 제목 (1~200자)
    - **content**: 내용
    """
    return post_crud.create_post(session, post, current_user_id)


@router.get("", response_model=dict)
def read_posts(
    pagination: Pagination = Depends(),
    session: Session = Depends(get_session)
):
    """
    게시글 목록을 페이지네이션으로 조회합니다.

    - **page**: 페이지 번호 (1부터 시작)
    - **size**: 페이지당 게시글 수 (최대 100)
    """
    posts = post_crud.get_posts(session, skip=pagination.skip, limit=pagination.size)
    total = post_crud.count_posts(session)

    return {
        "items": posts,
        "total": total,
        "page": pagination.page,
        "size": pagination.size,
        "pages": ceil(total / pagination.size) if pagination.size > 0 else 0
    }


@router.get("/{post_id}", response_model=PostResponse)
def read_post(post_id: int, session: Session = Depends(get_session)):
    """
    게시글을 조회합니다.

    조회 시 조회수가 1 증가합니다.
    """
    post = post_crud.get_post(session, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )

    # 조회수 증가
    post_crud.increment_views(session, post)

    return post


@router.patch("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    게시글을 수정합니다.

    작성자만 수정할 수 있습니다.
    """
    post = post_crud.get_post(session, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )

    # 작성자 확인
    if post.author_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="수정 권한이 없습니다"
        )

    return post_crud.update_post(session, post, post_update)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    게시글을 삭제합니다.

    작성자만 삭제할 수 있습니다.
    """
    post = post_crud.get_post(session, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )

    # 작성자 확인
    if post.author_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="삭제 권한이 없습니다"
        )

    post_crud.delete_post(session, post)
