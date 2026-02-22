from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import User


def test_create_user(client: TestClient):
    """사용자 생성 테스트"""
    response = client.post(
        "/users",
        json={
            "email": "new@example.com",
            "username": "신규사용자",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert data["username"] == "신규사용자"
    assert "id" in data
    assert "hashed_password" not in data  # 비밀번호는 응답에 없어야 함


def test_create_user_duplicate_email(client: TestClient, test_user: User):
    """중복 이메일로 사용자 생성 시 에러"""
    response = client.post(
        "/users",
        json={
            "email": test_user.email,  # 이미 존재하는 이메일
            "username": "다른사용자",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert "이미 등록된 이메일" in response.json()["detail"]


def test_read_users(client: TestClient, test_user: User):
    """사용자 목록 조회 테스트"""
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(user["email"] == test_user.email for user in data)


def test_read_user(client: TestClient, test_user: User):
    """사용자 상세 조회 테스트"""
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email


def test_read_user_not_found(client: TestClient):
    """존재하지 않는 사용자 조회 시 404"""
    response = client.get("/users/9999")
    assert response.status_code == 404
