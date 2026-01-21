from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import logging

from core.database import get_db
from .schemas import OrderCreate, OrderResponse, OrderStatusUpdate, OrderStatus, OrderListResponse
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
    

@router.get(
    "",
    response_model=list[OrderListResponse]
)
def list_orders_endpoint(
    db: Session = Depends(get_db),
    status: OrderStatus | None = None,
    customer_id: int | None = None
):
    orders = service.list_orders(db=db, status=status, customer_id=customer_id)
    if len(orders) == 0:
        logger.info("No orders found with the given filters")
        raise HTTPException(status_code=404, detail="No orders found")
    return orders

@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order_by_id_endpoint(order_id: int, db: Session = Depends(get_db)):
    order = service.get_order_by_id(db=db, order_id=order_id)
    if order is None:
        logger.info("Order ID=%s not found", order_id)
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return order


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse
)
def update_order_status_endpoint(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    try:
        order = service.update_order_status(db=db, order_id=order_id, new_status=payload.status)
        logger.info("Updated status of order ID=%s to %s", order_id, payload.status)
        return order
    except service.NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except service.BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))