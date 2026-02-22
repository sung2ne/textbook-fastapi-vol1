from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.post import Post


class CommentBase(SQLModel):
    """댓글 공통 필드"""
    content: str = Field(min_length=1, max_length=1000)


class CommentCreate(CommentBase):
    """댓글 작성 요청"""
    pass


class CommentUpdate(SQLModel):
    """댓글 수정 요청"""
    content: str = Field(min_length=1, max_length=1000)


class Comment(CommentBase, table=True):
    """댓글 테이블"""
    id: int | None = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="user.id")
    post_id: int = Field(foreign_key="post.id")
    created_at: datetime = Field(default_factory=datetime.now)

    # 관계 정의
    author: "User" = Relationship(back_populates="comments")
    post: "Post" = Relationship(back_populates="comments")


class CommentResponse(CommentBase):
    """댓글 응답"""
    id: int
    author_id: int
    post_id: int
    created_at: datetime
