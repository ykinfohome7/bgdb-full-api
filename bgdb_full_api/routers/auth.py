
from fastapi import APIRouter
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(username: str, password: str):
    # Demo placeholder
    return {"token": "demo-token", "user": username}
