import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import User, Post


@pytest.fixture(name="test_post")
def test_post_fixture(session: Session, test_user: User):
    """테스트용 게시글"""
    post = Post(
        title="테스트 게시글",
        content="테스트 내용입니다.",
        author_id=test_user.id
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def test_create_post(auth_client: TestClient):
    """게시글 생성 테스트"""
    response = auth_client.post(
        "/posts",
        json={
            "title": "새 게시글",
            "content": "새 내용입니다."
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "새 게시글"
    assert data["content"] == "새 내용입니다."
    assert "id" in data


def test_create_post_unauthorized(client: TestClient):
    """인증 없이 게시글 생성 시 401"""
    response = client.post(
        "/posts",
        json={
            "title": "새 게시글",
            "content": "새 내용입니다."
        }
    )
    assert response.status_code == 401


def test_read_posts(client: TestClient, test_post: Post):
    """게시글 목록 조회 테스트"""
    response = client.get("/posts")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] >= 1


def test_read_post(client: TestClient, test_post: Post):
    """게시글 상세 조회 테스트"""
    response = client.get(f"/posts/{test_post.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_post.id
    assert data["title"] == test_post.title


def test_read_post_increments_views(client: TestClient, test_post: Post):
    """게시글 조회 시 조회수 증가"""
    initial_response = client.get(f"/posts/{test_post.id}")
    initial_views = initial_response.json()["views"]

    second_response = client.get(f"/posts/{test_post.id}")
    new_views = second_response.json()["views"]

    assert new_views == initial_views + 1


def test_update_post(auth_client: TestClient, test_post: Post):
    """게시글 수정 테스트"""
    response = auth_client.patch(
        f"/posts/{test_post.id}",
        json={"title": "수정된 제목"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "수정된 제목"
    assert data["content"] == test_post.content  # 내용은 그대로


def test_update_post_not_author(
    client: TestClient,
    session: Session,
    test_post: Post
):
    """다른 사용자가 게시글 수정 시 403"""
    from app.models import User
    from app.security import get_password_hash, create_access_token

    # 다른 사용자 생성
    other_user = User(
        email="other@example.com",
        username="다른사용자",
        hashed_password=get_password_hash("password123")
    )
    session.add(other_user)
    session.commit()
    session.refresh(other_user)

    # 다른 사용자로 인증
    token = create_access_token(data={"sub": str(other_user.id)})
    client.headers["Authorization"] = f"Bearer {token}"

    response = client.patch(
        f"/posts/{test_post.id}",
        json={"title": "수정 시도"}
    )
    assert response.status_code == 403


def test_delete_post(auth_client: TestClient, test_post: Post):
    """게시글 삭제 테스트"""
    response = auth_client.delete(f"/posts/{test_post.id}")
    assert response.status_code == 204

    # 삭제 확인
    response = auth_client.get(f"/posts/{test_post.id}")
    assert response.status_code == 404


def test_read_post_not_found(client: TestClient):
    """존재하지 않는 게시글 조회 시 404"""
    response = client.get("/posts/9999")
    assert response.status_code == 404
