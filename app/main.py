from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import todos

app = FastAPI(
    title="TODO API",
    description="할 일 관리 API",
    version="1.0.0"
)

app.include_router(todos.router)


@app.get("/")
def read_root():
    return {"message": "TODO API에 오신 것을 환영합니다"}


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
