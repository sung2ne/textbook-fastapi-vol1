from fastapi import APIRouter

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("/")
def read_comments():
    return {"comments": []}
