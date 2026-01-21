from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from decimal import Decimal

from .models import Order, OrderItem, OrderStatus
from products.models import Product

from .schemas import OrderCreate, OrderResponse, OrderStatusUpdate

from customers.service import get_customer_by_id
from products.service import get_product_by_id

class NotFoundError(ValueError):
    pass

class BadRequestError(ValueError):
    pass


def create_order(db: Session, payload: OrderCreate) -> Order:
    # Validate items
    if not payload.items:
        raise BadRequestError("Order must contain at least one item")
    
    # Validate customr exists
    customer = get_customer_by_id(db=db, customer_id=payload.customer_id)
    if customer is None:
        raise NotFoundError(f"Customer with ID={payload.customer_id} not found")
    
    # Fetch all products in one query
    product_ids = [item.product_id for item in payload.items]
    products = db.execute(
        select(Product).where(Product.id.in_(product_ids))
    ).scalars().all()

    products_dict = {product.id: product for product in products}

    # Validate all products exists
    missing = set(product_ids) - set(products_dict.keys())
    if missing:
        raise NotFoundError(f"Products with IDs={missing} not found")
    
    # Create the order
    order = Order(
        customer_id=payload.customer_id,
        delivery_address=payload.delivery_address or customer.address, # if not speicified use customer's address
        status=OrderStatus.PENDING,
        total_price=Decimal("0.00")
    )
    
    db.add(order)
    db.flush()

    # Create items
    total = Decimal("0.00")

    for item_payload in payload.items:
        product = products_dict[item_payload.product_id]

        if product.in_stock < item_payload.quantity:
            raise BadRequestError(f"Insufficient stock for product ID={product.id},"
                            f"available={product.in_stock},"
                            f"requested={item_payload.quantity}")
        
        unit_price = Decimal(str(product.price))
        total += unit_price * item_payload.quantity

        order_item = OrderItem(
            order_id=order.id,
            product_id=item_payload.product_id,
            quantity=item_payload.quantity,
            unit_price=unit_price
        )

        db.add(order_item)
    
    order.total_price = total

    db.commit()
    
    # Reload order with items so response includes them
    order_with_items = db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order.id)
    ).scalar_one()

    return order_with_items


def list_orders(
    db: Session,
    status: OrderStatus | None = None,
    customer_id: int | None = None
) -> list[Order]:
    query = select(Order).order_by(Order.created_at.desc())

    if status:
        query = query.where(Order.status == status)

    if customer_id:
        query = query.where(Order.customer_id == customer_id)
    
    result = db.execute(query)
    orders = result.scalars().all()
    return orders


def get_order_by_id(db: Session, order_id: int) -> Order | None:
    result = db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    return order


def update_order_status(db: Session, order_id: int, new_status: OrderStatus) -> Order:
    # Retrieve the order
    order = db.execute(
        select(Order)
        .options(
            selectinload(Order.items)
            .selectinload(OrderItem.product)
        )
        .where(Order.id == order_id)
    ).scalar_one_or_none()

    if order is None:
        raise NotFoundError(f"Order with ID={order_id} not found")
    
    # Validate status transition:
    # PENDING -> CONFIRMED -> DELIVERED
    # PENDING -> CANCELLED
    valid_transitions = {
        OrderStatus.PENDING: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
        OrderStatus.CONFIRMED: {OrderStatus.DELIVERED},
        OrderStatus.DELIVERED: set(),
        OrderStatus.CANCELLED: set()
    }
    
    current_status = order.status

    if current_status == new_status:
        raise BadRequestError(f"Order already in status {new_status.value}")
    
    if new_status not in valid_transitions[current_status]:
        raise BadRequestError(
            f"Cannot change status from {current_status} to {new_status.value}"
        )
    
    # Stock update only when order is confirmed
    if new_status == OrderStatus.CONFIRMED:
        for item in order.items:
            product = item.product
            if product.in_stock < item.quantity:
                raise BadRequestError(
                    f"Insufficient stock for product ID={product.id},"
                    f"available={product.in_stock},"
                    f"requested={item.quantity}"
                )
            
        for item in order.items:
            item.product.in_stock -= item.quantity

    # Update status
    order.status = new_status

    db.commit()

    order = db.execute(
        select(Order)
        .options(
            selectinload(Order.items)
            .selectinload(OrderItem.product)
        )
        .where(Order.id == order_id)
    ).scalar_one()

    return order
            