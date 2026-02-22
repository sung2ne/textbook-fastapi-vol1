from fastapi import Depends, HTTPException, Query, status
from sqlmodel import Session
from app.database import get_session
from app.models import Post
from app.crud import post as post_crud


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
