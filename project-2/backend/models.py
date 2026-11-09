"""SQLAlchemy ORM models and pure domain logic for ShelfSync."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base

VALID_CATEGORIES = ("cold_chain", "reagent", "consumable")
ALLOWED_TRANSITIONS: dict[str, str] = {
    "requested": "approved",
    "approved": "fulfilled",
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def compute_stock_status(quantity: int, reorder_threshold: int) -> str:
    if quantity <= 0:
        return "critical_out"
    if quantity <= reorder_threshold:
        return "low_stock"
    return "healthy"


def validate_restock_transition(current_status: str, target_status: str) -> bool:
    return ALLOWED_TRANSITIONS.get(current_status) == target_status


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    category: Mapped[str] = mapped_column(String(32), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reorder_threshold: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    storage_temp_c: Mapped[float] = mapped_column(Float, nullable=False, default=4.0)
    supplier_email: Mapped[str] = mapped_column(String(160), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    def to_public_dict(self) -> dict:
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "reorder_threshold": self.reorder_threshold,
            "storage_temp_c": self.storage_temp_c,
            "stock_status": compute_stock_status(self.quantity, self.reorder_threshold),
            "updated_at": self.updated_at.isoformat(),
        }


class RestockOrder(Base):
    __tablename__ = "restock_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    order_qty: Mapped[int] = mapped_column(Integer, nullable=False)
    requested_by: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="requested")
    trace_id: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "sku": self.sku,
            "order_qty": self.order_qty,
            "requested_by": self.requested_by,
            "status": self.status,
            "trace_id": self.trace_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class StockLedgerEvent(Base):
    __tablename__ = "stock_ledger_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    delta: Mapped[int] = mapped_column(Integer, nullable=False)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False)
    note: Mapped[str] = mapped_column(String(160), nullable=False)
    trace_id: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now
    )
