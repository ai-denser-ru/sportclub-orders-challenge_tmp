"""Pydantic schemas for the Order entity."""

from datetime import date

from pydantic import BaseModel, ConfigDict

from app.models.enums import OrderStatus
from app.schemas.customer import CustomerRead
from app.schemas.order_item import OrderItemCreate, OrderItemRead


class OrderBase(BaseModel):
    """Shared fields for Order schemas."""

    customer_id: int
    date: date
    status: OrderStatus = OrderStatus.PENDING


class OrderCreate(OrderBase):
    """Schema for creating a new Order with nested items."""

    items: list[OrderItemCreate]


class OrderRead(BaseModel):
    """Schema for returning an Order summary in list views."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    date: date
    status: OrderStatus
    total: float


class OrderDetail(OrderRead):
    """Schema for returning a detailed Order with customer and items."""

    customer: CustomerRead
    items: list[OrderItemRead]


class OrderStatusUpdate(BaseModel):
    """Schema for PATCH /orders/{id}/status."""

    status: OrderStatus
