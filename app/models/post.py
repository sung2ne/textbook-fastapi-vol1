from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.comment import Comment


class PostBase(SQLModel):
    """게시글 공통 필드"""
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    """게시글 작성 요청"""
    pass


class PostUpdate(SQLModel):
    """게시글 수정 요청"""
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1)


class Post(PostBase, table=True):
    """게시글 테이블"""
    id: int | None = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="user.id")
    views: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None

    # 관계 정의
    author: "User" = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post")


class PostResponse(PostBase):
    """게시글 응답"""
    id: int
    author_id: int
    views: int
    created_at: datetime
    updated_at: datetime | None


class PostListResponse(SQLModel):
    """게시글 목록 응답 (간략 정보)"""
    id: int
    title: str
    author_id: int
    views: int
    created_at: datetime
