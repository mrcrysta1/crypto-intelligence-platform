import uuid

from sqlalchemy import Boolean, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class Asset(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "assets"

    symbol: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    market_cap_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    circulating_supply: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_supply: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_supply: Mapped[float | None] = mapped_column(Float, nullable=True)
    ath: Mapped[float | None] = mapped_column(Float, nullable=True)
    ath_change: Mapped[float | None] = mapped_column(Float, nullable=True)

    def __repr__(self) -> str:
        return f"<Asset {self.symbol} ({self.name})>"


class Exchange(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "exchanges"

    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    api_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Exchange {self.name}>"


class Market(Base, UUIDMixin):
    __tablename__ = "markets"

    exchange_name: Mapped[str] = mapped_column(String(128), nullable=False)
    pair: Mapped[str] = mapped_column(String(64), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )

    def __repr__(self) -> str:
        return f"<Market {self.pair}@{self.exchange_name}>"
