from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: Decimal
    in_stock: int

class ProductCreate(ProductBase):
    pass 

class ProductUpdate(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    in_stock: int | None = None

class ProductResponse(ProductBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True