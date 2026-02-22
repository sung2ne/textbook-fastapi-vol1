from datetime import datetime
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.models import Post, PostCreate, PostUpdate


def create_post(session: Session, post_create: PostCreate, author_id: int) -> Post:
    """게시글 생성"""
    post = Post(
        title=post_create.title,
        content=post_create.content,
        author_id=author_id
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def get_posts(
    session: Session,
    skip: int = 0,
    limit: int = 10
) -> list[Post]:
    """게시글 목록 조회"""
    statement = (
        select(Post)
        .options(selectinload(Post.author))  # 작성자 정보 미리 로드
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return session.exec(statement).all()


def get_post(session: Session, post_id: int) -> Post | None:
    """게시글 상세 조회"""
    statement = (
        select(Post)
        .options(selectinload(Post.author))
        .where(Post.id == post_id)
    )
    return session.exec(statement).first()


def update_post(session: Session, post: Post, post_update: PostUpdate) -> Post:
    """게시글 수정"""
    update_data = post_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(post, key, value)

    post.updated_at = datetime.now()

    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def delete_post(session: Session, post: Post) -> None:
    """게시글 삭제"""
    session.delete(post)
    session.commit()


def increment_views(session: Session, post: Post) -> Post:
    """조회수 증가"""
    post.views += 1
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def count_posts(session: Session) -> int:
    """게시글 총 개수"""
    statement = select(Post)
    return len(session.exec(statement).all())
