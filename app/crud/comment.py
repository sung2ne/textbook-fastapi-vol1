from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.models import Comment, CommentCreate, CommentUpdate


def create_comment(
    session: Session,
    comment_create: CommentCreate,
    post_id: int,
    author_id: int
) -> Comment:
    """댓글 생성"""
    comment = Comment(
        content=comment_create.content,
        post_id=post_id,
        author_id=author_id
    )
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


def get_comments_by_post(
    session: Session,
    post_id: int,
    skip: int = 0,
    limit: int = 50
) -> list[Comment]:
    """게시글의 댓글 목록 조회"""
    statement = (
        select(Comment)
        .options(selectinload(Comment.author))
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
        .offset(skip)
        .limit(limit)
    )
    return session.exec(statement).all()


def get_comment(session: Session, comment_id: int) -> Comment | None:
    """댓글 조회"""
    return session.get(Comment, comment_id)


def update_comment(
    session: Session,
    comment: Comment,
    comment_update: CommentUpdate
) -> Comment:
    """댓글 수정"""
    comment.content = comment_update.content
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


def delete_comment(session: Session, comment: Comment) -> None:
    """댓글 삭제"""
    session.delete(comment)
    session.commit()


def count_comments_by_post(session: Session, post_id: int) -> int:
    """게시글의 댓글 수"""
    statement = select(Comment).where(Comment.post_id == post_id)
    return len(session.exec(statement).all())
