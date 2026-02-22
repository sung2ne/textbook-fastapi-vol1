from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session
from app.database import get_session
from app.dependencies import get_current_active_user
from app.models import User, CommentCreate, CommentUpdate, CommentResponse, PaginatedResponse
from app.crud import comment as comment_crud, post as post_crud

router = APIRouter(tags=["comments"])


@router.post(
    "/posts/{post_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_comment(
    post_id: int,
    comment: CommentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    게시글에 댓글을 작성합니다.

    **인증 필요**
    """
    post = post_crud.get_post(session, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )

    return comment_crud.create_comment(session, comment, post_id, current_user.id)


@router.get("/posts/{post_id}/comments", response_model=PaginatedResponse[CommentResponse])
def read_comments(
    post_id: int,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session)
):
    """
    게시글의 댓글 목록을 조회합니다.

    **인증 불필요**
    """
    post = post_crud.get_post(session, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )

    skip = (page - 1) * size
    comments = comment_crud.get_comments_by_post(session, post_id, skip, size)
    total = comment_crud.count_comments_by_post(session, post_id)

    return {
        "items": comments,
        "total": total,
        "page": page,
        "size": size,
        "pages": ceil(total / size) if size > 0 else 0
    }


@router.patch("/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    댓글을 수정합니다.

    **인증 필요** - 작성자만 수정 가능
    """
    comment = comment_crud.get_comment(session, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다"
        )

    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="수정 권한이 없습니다"
        )

    return comment_crud.update_comment(session, comment, comment_update)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    댓글을 삭제합니다.

    **인증 필요** - 작성자만 삭제 가능
    """
    comment = comment_crud.get_comment(session, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다"
        )

    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="삭제 권한이 없습니다"
        )

    comment_crud.delete_comment(session, comment)
