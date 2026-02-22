from fastapi.testclient import TestClient
from sqlmodel import Session
from jose import jwt

from app.models import User
from app.config import settings


def test_login_success(client: TestClient, test_user: User):
    """정상 로그인 테스트"""
    response = client.post(
        "/auth/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_email(client: TestClient):
    """잘못된 이메일로 로그인 시 401"""
    response = client.post(
        "/auth/login",
        data={
            "username": "wrong@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 401
    assert "이메일 또는 비밀번호" in response.json()["detail"]


def test_login_wrong_password(client: TestClient, test_user: User):
    """잘못된 비밀번호로 로그인 시 401"""
    response = client.post(
        "/auth/login",
        data={
            "username": test_user.email,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401


def test_read_me(auth_client: TestClient, test_user: User):
    """내 정보 조회 테스트"""
    response = auth_client.get("/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email


def test_read_me_unauthorized(client: TestClient):
    """인증 없이 내 정보 조회 시 401"""
    response = client.get("/users/me")
    assert response.status_code == 401


def test_read_me_invalid_token(client: TestClient):
    """잘못된 토큰으로 요청 시 401"""
    client.headers["Authorization"] = "Bearer invalid_token"
    response = client.get("/users/me")
    assert response.status_code == 401


def test_read_me_expired_token(client: TestClient, test_user: User):
    """만료된 토큰으로 요청 시 401"""
    from datetime import timedelta
    from app.security import create_access_token

    # 이미 만료된 토큰 생성
    token = create_access_token(
        data={"sub": str(test_user.id)},
        expires_delta=timedelta(seconds=-1)  # 이미 만료
    )
    client.headers["Authorization"] = f"Bearer {token}"

    response = client.get("/users/me")
    assert response.status_code == 401


def test_inactive_user_cannot_access(
    client: TestClient,
    session: Session,
    test_user: User
):
    """비활성 사용자는 접근 불가"""
    from app.security import create_access_token

    # 사용자 비활성화
    test_user.is_active = False
    session.add(test_user)
    session.commit()

    # 토큰은 유효하지만 비활성 사용자
    token = create_access_token(data={"sub": str(test_user.id)})
    client.headers["Authorization"] = f"Bearer {token}"

    response = client.get("/users/me")
    assert response.status_code == 403
    assert "비활성화된 계정" in response.json()["detail"]


def test_token_contains_user_id(client: TestClient, test_user: User):
    """토큰에 사용자 ID가 포함되어 있는지 확인"""
    response = client.post(
        "/auth/login",
        data={
            "username": test_user.email,
            "password": "password123"
        }
    )
    token = response.json()["access_token"]

    # 토큰 디코딩
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )

    assert payload["sub"] == str(test_user.id)
    assert "exp" in payload  # 만료 시간 존재
