from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    price: float

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

class ItemOut(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
