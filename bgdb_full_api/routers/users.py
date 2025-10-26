
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from ..database import SessionLocal, Base, engine
from ..models.user import User

# Create tables if not exist (simple demo)
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    email: EmailStr

@router.get("")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("", status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter((User.username == payload.username) | (User.email == payload.email)).first()
    if exists:
        raise HTTPException(status_code=409, detail="User with same username/email exists")
    u = User(username=payload.username, email=payload.email)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u
