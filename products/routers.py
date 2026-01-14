from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database import get_db
from .schemas import ProductCreate, ProductResponse
from . import service

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product_endpoint(
    payload: ProductCreate,
    db: Session = Depends(get_db)
):
    product = service.create_product(db=db, payload=payload)
    return product

@router.get(
    "",
    response_model=list[ProductResponse],
)
def list_products_endpoint(db: Session = Depends(get_db)):
    products = service.list_products(db=db)
    return products

