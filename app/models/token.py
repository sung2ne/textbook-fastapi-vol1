from pydantic import BaseModel


class Token(BaseModel):
    """토큰 응답"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """토큰에서 추출한 데이터"""
    user_id: int | None = None
