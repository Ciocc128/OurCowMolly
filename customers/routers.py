from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm  import Session
import logging

from core.database import get_db
from .schemas import CustomerCreate, CustomerResponse, CustomerUpdate
from . import service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer_endpoint(
    payload: CustomerCreate,
    db: Session = Depends(get_db)
):
    customer = service.create_customers(db=db, payload=payload)
    logger.info("Created customer ID=%s: name=%s", customer.id, customer.name)
    return customer


@router.get(
    "",
    response_model=list[CustomerResponse]
)
def list_customers_endpoint(db: Session = Depends(get_db)):
    customers = service.list_customers(db=db)
    return customers


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer_by_id_endpoint(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = service.get_customer_by_id(db=db, customer_id=customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
    return customer

    