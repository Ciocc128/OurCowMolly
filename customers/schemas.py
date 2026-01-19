from pydantic import BaseModel
from datetime import datetime

class MessageResponse(BaseModel):
    message: str

class CustomerBase(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    address: str

class CustomerCreate(CustomerBase):
    pass 

class CustomerUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None

class CustomerResponse(CustomerBase):
    id: int
    registered_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    