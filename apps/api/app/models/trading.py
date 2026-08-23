from sqlalchemy import Column, String, Float, DateTime, Boolean
from app.models.base import Base
import datetime

class PaperOrder(Base):
    __tablename__ = "paper_orders"
    id = Column(String, primary_key=True)
    asset_id = Column(String)
    order_type = Column(String)  # market, limit
    side = Column(String)  # buy, sell
    amount_usd = Column(Float)
    price = Column(Float)
    status = Column(String)  # filled, cancelled, pending
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    filled_at = Column(DateTime)

class PaperPosition(Base):
    __tablename__ = "paper_positions"
    id = Column(String, primary_key=True)
    asset_id = Column(String)
    side = Column(String)  # long, short
    entry_price = Column(Float)
    current_price = Column(Float)
    size_usd = Column(Float)
    unrealized_pnl = Column(Float)
    realized_pnl = Column(Float, default=0)
    opened_at = Column(DateTime, default=datetime.datetime.utcnow)
    closed_at = Column(DateTime)

class PaperPortfolio(Base):
    __tablename__ = "paper_portfolio"
    id = Column(String, primary_key=True)
    cash_balance = Column(Float, default=100000)
    total_value = Column(Float, default=100000)
    unrealized_pnl = Column(Float, default=0)
    realized_pnl = Column(Float, default=0)
    positions_count = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
