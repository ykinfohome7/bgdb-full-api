from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.database import SessionLocal
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["users"])
bearer = HTTPBearer(auto_error=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_id_from_token(creds: HTTPAuthorizationCredentials) -> int:
    try:
        data = jwt.decode(creds.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if data.get("type") != "access":
            raise JWTError("Invalid token type")
        return int(data.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.get("/me", response_model=UserOut)
def me(creds: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(creds)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
