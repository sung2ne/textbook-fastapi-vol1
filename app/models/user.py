from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.post import Post
    from app.models.comment import Comment


class UserBase(SQLModel):
    """사용자 공통 필드"""
    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(max_length=50)


class UserCreate(UserBase):
    """회원가입 요청"""
    password: str = Field(min_length=8)


class UserUpdate(SQLModel):
    """사용자 정보 수정"""
    username: str | None = Field(default=None, max_length=50)
    password: str | None = Field(default=None, min_length=8)


class User(UserBase, table=True):
    """사용자 테이블"""
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)

    # 관계 정의
    posts: list["Post"] = Relationship(back_populates="author")
    comments: list["Comment"] = Relationship(back_populates="author")


class UserResponse(UserBase):
    """사용자 응답 (비밀번호 제외)"""
    id: int
    is_active: bool
    created_at: datetime
