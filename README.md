# 소설처럼 읽는 FastAPI Vol.1

> **TODO 앱과 게시판으로 배우는 현대적 Python API 개발**

이 저장소는 교재 [소설처럼 읽는 FastAPI Vol.1](https://text.ibetter.kr/fastapi-vol1)의 챕터별 실습 코드입니다.

## 브랜치 구조

각 브랜치에는 해당 챕터까지의 누적 코드가 포함됩니다.

- `part05/chapter-01` ~ `part11/chapter-04`: 코드 챕터별 브랜치
- `main`: 최종 완성 코드

## 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 개발 서버 실행
uvicorn main:app --reload
```
