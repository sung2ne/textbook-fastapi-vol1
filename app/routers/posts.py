from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session
from app.database import get_session
from app.dependencies import get_current_active_user, Pagination
from app.models import User, Post, PostCreate, PostUpdate, PostResponse, PostListResponse, PaginatedResponse
from app.crud import post as post_crud

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    게시글을 작성합니다.

    **인증 필요**
    """
    return post_crud.create_post(session, post, current_user.id)


@router.get("", response_model=PaginatedResponse[PostListResponse])
def read_posts(
    pagination: Pagination = Depends(),
    session: Session = Depends(get_session)
):
    """
    게시글 목록을 조회합니다.

    **인증 불필요**
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
def read_post(
    post_id: int,
    session: Session = Depends(get_session)
):
    """
    게시글을 조회합니다.

    **인증 불필요**
    """
    post = post_crud.get_post(session, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )

    post_crud.increment_views(session, post)
    return post


@router.patch("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    게시글을 수정합니다.

    **인증 필요** - 작성자만 수정 가능
    """
    post = post_crud.get_post(session, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )

    # 작성자 확인
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="수정 권한이 없습니다"
        )

    return post_crud.update_post(session, post, post_update)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    게시글을 삭제합니다.

    **인증 필요** - 작성자만 삭제 가능
    """
    post = post_crud.get_post(session, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="삭제 권한이 없습니다"
        )

    post_crud.delete_post(session, post)
