from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import logging

from core.database import get_db
from .schemas import ProductCreate, ProductResponse, ProductUpdate, MessageResponse
from . import service

logger = logging.getLogger(__name__)

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
    print(f"[DEBUG] Received payload: {payload}")  # Debug: mostra i dati ricevuti dal client
    product = service.create_product(db=db, payload=payload)
    logger.info("Created product ID=%s name=%s", product.id, product.name)
    return product


@router.get(
    "",
    response_model=list[ProductResponse],
)
def list_products_endpoint(db: Session = Depends(get_db)):
    products = service.list_products(db=db)
    return products


#TODO Handle the edge cases
@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product_by_id_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = service.get_product_by_id(db=db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product with ID={product_id} not found")
    return product

@router.patch(
    "/{product_id}",
    response_model=ProductResponse  
)
def update_product_endpoint(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = service.update_product(db=db, product_id=product_id, payload=payload)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product with ID={product_id} not found")
    
    logger.info("Updated product ID=%s", product_id)
    return product

@router.delete(
    "/{product_id}",
    response_model=MessageResponse
)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = service.delete_product(db=db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product with ID={product_id} not found")
    
    logger.info("Product ID=%s deleted successfully!", product_id)
    return {"message": f"Product with ID={product_id} successfully deleted!"}