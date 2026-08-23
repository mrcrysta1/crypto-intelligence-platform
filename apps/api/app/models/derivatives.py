import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class FundingRate(Base, UUIDMixin):
    __tablename__ = "funding_rates"

    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    exchange_name: Mapped[str] = mapped_column(String(128), nullable=False)
    funding_rate: Mapped[float] = mapped_column(Float, nullable=False)
    predicted_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )


class OpenInterest(Base, UUIDMixin):
    __tablename__ = "open_interests"

    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    exchange_name: Mapped[str] = mapped_column(String(128), nullable=False)
    open_interest: Mapped[float] = mapped_column(Float, nullable=False)
    open_interest_change_24h: Mapped[float | None] = mapped_column(Float, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )


class Liquidation(Base, UUIDMixin):
    __tablename__ = "liquidations"

    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    exchange_name: Mapped[str] = mapped_column(String(128), nullable=False)
    side: Mapped[str] = mapped_column(String(8), nullable=False)
    amount_usd: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )
