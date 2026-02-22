from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session
from app.database import get_session
from app.models import Comment, CommentCreate, CommentUpdate, CommentResponse, PaginatedResponse
from app.crud import comment as comment_crud, post as post_crud
from app.dependencies import Pagination

router = APIRouter(tags=["comments"])


# 임시: 로그인한 사용자 ID
def get_current_user_id() -> int:
    return 1


@router.post(
    "/posts/{post_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_comment(
    post_id: int,
    comment: CommentCreate,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    게시글에 댓글을 작성합니다.
    """
    # 게시글 존재 확인
    post = post_crud.get_post(session, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )

    return comment_crud.create_comment(session, comment, post_id, current_user_id)


@router.get("/posts/{post_id}/comments", response_model=PaginatedResponse[CommentResponse])
def read_comments(
    post_id: int,
    pagination: Pagination = Depends(),
    session: Session = Depends(get_session)
):
    """
    게시글의 댓글을 페이지네이션으로 조회합니다.
    """
    post = post_crud.get_post(session, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )

    comments = comment_crud.get_comments_by_post(session, post_id, pagination.skip, pagination.size)
    total = comment_crud.count_comments_by_post(session, post_id)

    return {
        "items": comments,
        "total": total,
        "page": pagination.page,
        "size": pagination.size,
        "pages": ceil(total / pagination.size) if pagination.size > 0 else 0
    }


@router.patch("/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    댓글을 수정합니다.

    작성자만 수정할 수 있습니다.
    """
    comment = comment_crud.get_comment(session, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다"
        )

    if comment.author_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="수정 권한이 없습니다"
        )

    return comment_crud.update_comment(session, comment, comment_update)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    댓글을 삭제합니다.

    작성자만 삭제할 수 있습니다.
    """
    comment = comment_crud.get_comment(session, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다"
        )

    if comment.author_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="삭제 권한이 없습니다"
        )

    comment_crud.delete_comment(session, comment)
