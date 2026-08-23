import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class SignalDirection(str, enum.Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    WATCH = "WATCH"
    NO_TRADE = "NO_TRADE"


class RiskLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Signal(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "signals"

    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    direction: Mapped[SignalDirection] = mapped_column(
        Enum(SignalDirection, name="signal_direction", native_enum=False),
        nullable=False,
    )
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    reasons: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    technical_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    fundamental_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    whale_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    derivative_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    composite_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk_level: Mapped[RiskLevel | None] = mapped_column(
        Enum(RiskLevel, name="signal_risk_level", native_enum=False), nullable=True
    )
    model_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )

    def __repr__(self) -> str:
        return f"<Signal asset={self.asset_id} direction={self.direction} conf={self.confidence}>"


class AssetScore(Base, UUIDMixin):
    __tablename__ = "asset_scores"

    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    fundamental_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    technical_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    whale_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    derivative_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    composite_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk_level: Mapped[str | None] = mapped_column(String(16), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )


class Ranking(Base, UUIDMixin):
    __tablename__ = "rankings"

    rank: Mapped[int] = mapped_column(nullable=False)
    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    composite_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    direction: Mapped[str | None] = mapped_column(String(16), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
