import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class WalletLabel(str, enum.Enum):
    EXCHANGE = "EXCHANGE"
    WHALE = "WHALE"
    TREASURY = "TREASURY"
    BURN_ADDRESS = "BURN_ADDRESS"
    OTHER = "OTHER"


class Wallet(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "wallets"

    address: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    label: Mapped[WalletLabel] = mapped_column(
        Enum(WalletLabel, name="wallet_label", native_enum=False),
        default=WalletLabel.OTHER,
        nullable=False,
    )
    asset_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("assets.id", ondelete="SET NULL"), nullable=True
    )
    balance_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_active: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<Wallet {self.address[:16]}... label={self.label}>"


class WalletTransaction(Base, UUIDMixin):
    __tablename__ = "wallet_transactions"

    wallet_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("wallets.id", ondelete="CASCADE"), nullable=True
    )
    asset_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("assets.id", ondelete="SET NULL"), nullable=True
    )
    tx_hash: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    from_address: Mapped[str] = mapped_column(String(255), nullable=False)
    to_address: Mapped[str] = mapped_column(String(255), nullable=False)
    amount_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )
    tx_type: Mapped[str | None] = mapped_column(String(64), nullable=True)


class WhaleEvent(Base, UUIDMixin):
    __tablename__ = "whale_events"

    EVENT_TYPES = ("large_transfer", "accumulation", "distribution")

    asset_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=True, index=True
    )
    wallet_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("wallets.id", ondelete="SET NULL"), nullable=True
    )
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    amount_usd: Mapped[float] = mapped_column(Float, nullable=False)
    from_address: Mapped[str] = mapped_column(String(255), nullable=False)
    to_address: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )


class ExchangeFlow(Base, UUIDMixin):
    __tablename__ = "exchange_flows"

    flow_type: Mapped[str] = mapped_column(String(16), nullable=False)
    asset_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=True, index=True
    )
    exchange_name: Mapped[str] = mapped_column(String(128), nullable=False)
    amount_usd: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )
