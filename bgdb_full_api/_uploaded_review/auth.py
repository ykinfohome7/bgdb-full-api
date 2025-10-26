from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app.core.database import SessionLocal
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.core.config import settings
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut, status_code=201)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == user_in.email).first()
    if exists:
        raise HTTPException(status_code=409, detail="User already exists")
    user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password), full_name=user_in.full_name or "")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

@router.post("/refresh")
def refresh(token: str):
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if data.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = data.get("sub")
        new_access = create_access_token(user_id)
        return {"access_token": new_access, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
