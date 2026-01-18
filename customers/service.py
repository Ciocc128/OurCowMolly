from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import Customer
from .schemas import CustomerCreate, CustomerResponse, CustomerUpdate


def create_customers(db: Session, payload: CustomerCreate):
    customer = Customer(
        name = payload.name,
        address = payload.address,
        email = payload.email if payload.email else None,
        phone = payload.phone if payload.phone else None
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def list_customers(db: Session):
    result = db.execute(select(Customer).order_by(Customer.name))
    customers = result.scalars().all()
    return customers


def get_customer_by_id(db: Session, customer_id: int):
    result = db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    return customer