from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
def hello():
    return {"message": "[FastAPI] Connected to connection file."}