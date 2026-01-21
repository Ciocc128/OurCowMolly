from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import logging

from core.database import get_db
from .schemas import OrderCreate, OrderResponse, OrderStatusUpdate
from . import service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Bad Request"},
        404: {"description": "Not Found"}
    }
)
def create_order_endpoint(payload: OrderCreate, db: Session = Depends(get_db)):
    try:
        order = service.create_order(db=db, payload=payload)
        logger.info("Created order ID=%s for customer ID=%s", order.id, order.customer_id)
        return order
    except service.NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except service.BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))