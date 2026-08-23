import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class Price(Base, UUIDMixin):
    __tablename__ = "prices"

    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    exchange_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("exchanges.id", ondelete="SET NULL"), nullable=True
    )
    price: Mapped[float] = mapped_column(Float, nullable=False)
    volume_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    change_1h: Mapped[float | None] = mapped_column(Float, nullable=True)
    change_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    change_7d: Mapped[float | None] = mapped_column(Float, nullable=True)
    change_30d: Mapped[float | None] = mapped_column(Float, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )

    def __repr__(self) -> str:
        return f"<Price asset={self.asset_id} price={self.price}>"


class OHLCV(Base, UUIDMixin):
    __tablename__ = "ohlcvs"

    INTERVALS = ("1m", "5m", "15m", "1h", "4h", "1d")

    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    exchange_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("exchanges.id", ondelete="SET NULL"), nullable=True
    )
    interval: Mapped[str] = mapped_column(String(8), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"<OHLCV asset={self.asset_id} interval={self.interval}>"


class Trade(Base, UUIDMixin):
    __tablename__ = "trades"

    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    exchange_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("exchanges.id", ondelete="SET NULL"), nullable=True
    )
    side: Mapped[str] = mapped_column(String(8), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )


class OrderBook(Base, UUIDMixin):
    __tablename__ = "order_books"

    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    exchange_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("exchanges.id", ondelete="SET NULL"), nullable=True
    )
    bids: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    asks: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )
