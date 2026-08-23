import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class NewsArticle(Base, UUIDMixin):
    __tablename__ = "news_articles"

    title: Mapped[str] = mapped_column(String(512), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), unique=True, nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sentiment: Mapped[float | None] = mapped_column(Float, nullable=True)
    impact: Mapped[str | None] = mapped_column(String(16), default="medium", nullable=True)
    summary: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    related_assets: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    categories: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )

    def __repr__(self) -> str:
        return f"<NewsArticle {self.title[:50]}>"
