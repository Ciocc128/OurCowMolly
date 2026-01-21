from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from decimal import Decimal

from .models import Order, OrderItem, OrderStatus
from products.models import Product

from .schemas import OrderCreate, OrderResponse, OrderStatusUpdate

from customers.service import get_customer_by_id

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

        
        