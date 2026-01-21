from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

from .models import OrderStatus

# ----------- Order Items -----------

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderItemCreate(OrderItemBase):
    pass 

class OrderItemResponse(OrderItemBase):
    id: int
    unit_price: Decimal

    class Config:
        from_attributes = True

# ----------- Orders -----------

class OrderBase(BaseModel):
    customer_id: int
    delivery_address: str
    

class OrderCreate(OrderBase):
    items: list[OrderItemCreate] 

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderResponse(OrderBase):
    id: int
    total_price: Decimal
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True