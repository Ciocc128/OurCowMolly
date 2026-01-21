from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from decimal import Decimal
import enum

from core.database import Base

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)

    total_price = Column(Numeric(10,2), nullable=False, default=Decimal("0.00"))

    status = Column(
        Enum(OrderStatus, name="order_status"),
        nullable=False,
        default=OrderStatus.PENDING,
        index=True
    )

    delivery_address = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # ORM relationships
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Order id={self.id} customer_id={self.customer_id} status={self.status} total_price={self.total_price}"

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)

    quantity = Column(Integer, nullable=False)

    unit_price = Column(Numeric(10,2), nullable=False)

    # ORM relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items", lazy="selectin")

    def __repr__(self) -> str:
        return f"<OrderItem id={self.id} order_id={self.order_id} product_id={self.product_id} quantity={self.quantity} unit_price={self.unit_price}>"
