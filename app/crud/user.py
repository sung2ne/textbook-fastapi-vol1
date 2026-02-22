from sqlmodel import Session, select
from app.models import User, UserCreate, UserUpdate
from app.security import get_password_hash, verify_password


def create_user(session: Session, user_create: UserCreate) -> User:
    """사용자 생성"""
    hashed_password = get_password_hash(user_create.password)
    user = User(
        email=user_create.email,
        username=user_create.username,
        hashed_password=hashed_password
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_email(session: Session, email: str) -> User | None:
    """이메일로 사용자 조회"""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user(session: Session, user_id: int) -> User | None:
    """ID로 사용자 조회"""
    return session.get(User, user_id)


def get_users(session: Session, skip: int = 0, limit: int = 10) -> list[User]:
    """사용자 목록 조회"""
    statement = select(User).offset(skip).limit(limit)
    return session.exec(statement).all()


def update_user(session: Session, user: User, user_update: UserUpdate) -> User:
    """사용자 정보 수정"""
    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    """사용자 인증 (로그인용)"""
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
