"""API router for Order endpoints."""

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.enums import OrderStatus
from app.schemas.order import (
    OrderCreate,
    OrderDetail,
    OrderRead,
    OrderStatusUpdate,
)
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


def _get_service(db: Session = Depends(get_db)) -> OrderService:
    """Dependency to inject OrderService."""
    return OrderService(db)


@router.get("", response_model=list[OrderRead])
def list_orders(
    status: OrderStatus | None = Query(None, description="Filter by order status"),
    dateFrom: date | None = Query(None, alias="dateFrom", description="Start date"),
    dateTo: date | None = Query(None, alias="dateTo", description="End date"),
    service: OrderService = Depends(_get_service),
) -> list[OrderRead]:
    """Return filtered list of orders."""
    orders = service.list_orders(status=status, date_from=dateFrom, date_to=dateTo)
    return [OrderRead.model_validate(o) for o in orders]


@router.get("/{order_id}", response_model=OrderDetail)
def get_order(
    order_id: int,
    service: OrderService = Depends(_get_service),
) -> OrderDetail:
    """Return order details including customer and items."""
    order = service.get_order(order_id)
    return OrderDetail.model_validate(order)


@router.post("", response_model=OrderRead, status_code=201)
def create_order(
    data: OrderCreate,
    service: OrderService = Depends(_get_service),
) -> OrderRead:
    """Create a new order with items."""
    order = service.create_order(data)
    return OrderRead.model_validate(order)


@router.patch("/{order_id}/status", response_model=OrderRead)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    service: OrderService = Depends(_get_service),
) -> OrderRead:
    """Update the status of an existing order."""
    order = service.update_status(order_id, data)
    return OrderRead.model_validate(order)
