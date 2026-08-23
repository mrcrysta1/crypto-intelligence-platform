import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class SocialPost(Base, UUIDMixin):
    __tablename__ = "social_posts"

    platform: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    content: Mapped[str] = mapped_column(String(4096), nullable=False)
    sentiment: Mapped[float | None] = mapped_column(Float, nullable=True)
    engagement_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    related_assets: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )


class SentimentScore(Base, UUIDMixin):
    __tablename__ = "sentiment_scores"

    asset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    platform: Mapped[str] = mapped_column(String(32), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )
