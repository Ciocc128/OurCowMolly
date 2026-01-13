from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

from .models import OrderStatus

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass 

class OrderItemResponse(OrderItemBase):
    id: int

    class Config:
        from_attributes = True

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