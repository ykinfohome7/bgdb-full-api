from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from jose import jwt, JWTError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.database import SessionLocal
from app.core.config import settings
from app.models.item import Item
from app.models.user import User
from app.schemas.item import ItemCreate, ItemUpdate, ItemOut

router = APIRouter(prefix="/items", tags=["items"])
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

@router.get("", response_model=List[ItemOut])
def list_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

@router.post("", response_model=ItemOut, status_code=201)
def create_item(item: ItemCreate, creds: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(creds)
    owner = db.query(User).filter(User.id == user_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    obj = Item(name=item.name, price=item.price, owner_id=owner.id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(Item).filter(Item.id == item_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    return obj

@router.put("/{item_id}", response_model=ItemOut)
def update_item(item_id: int, payload: ItemUpdate, creds: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    _ = get_user_id_from_token(creds)
    obj = db.query(Item).filter(Item.id == item_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    if payload.name is not None:
        obj.name = payload.name
    if payload.price is not None:
        obj.price = payload.price
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, creds: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    _ = get_user_id_from_token(creds)
    obj = db.query(Item).filter(Item.id == item_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(obj)
    db.commit()
    return None
