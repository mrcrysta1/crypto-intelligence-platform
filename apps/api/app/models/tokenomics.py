import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class Tokenomics(Base, UUIDMixin):
    __tablename__ = "tokenomics"

    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    total_supply: Mapped[float | None] = mapped_column(Float, nullable=True)
    circulating_supply: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_supply: Mapped[float | None] = mapped_column(Float, nullable=True)
    allocation: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    vesting_schedule: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class TokenUnlock(Base, UUIDMixin):
    __tablename__ = "token_unlocks"

    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    event_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    usd_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    unlock_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    percentage_of_supply: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )

    def __repr__(self) -> str:
        return f"<TokenUnlock asset={self.asset_id} type={self.event_type}>"
