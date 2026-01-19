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


def update_customer(db: Session, customer_id: int, payload: CustomerUpdate) -> Customer | None:
    customer = get_customer_by_id(db=db, customer_id=customer_id)
    
    if customer is None:
        return None
    
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(customer, field, value)
    
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int):
    result = db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()

    if customer is None:
        return None
    
    db.delete(customer)
    db.commit()
    return {"message": f"Customer with ID={customer_id} successfully deleted!"}
