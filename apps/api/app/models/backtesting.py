from sqlalchemy import Column, String, Float, Integer, DateTime, JSON
from app.models.base import Base
import datetime

class Backtest(Base):
    __tablename__ = "backtests"
    id = Column(String, primary_key=True)
    asset_id = Column(String)
    strategy_name = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    initial_capital = Column(Float)
    final_capital = Column(Float)
    total_return = Column(Float)
    sharpe_ratio = Column(Float)
    max_drawdown = Column(Float)
    win_rate = Column(Float)
    total_trades = Column(Integer)
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Strategy(Base):
    __tablename__ = "strategies"
    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    parameters_schema = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
