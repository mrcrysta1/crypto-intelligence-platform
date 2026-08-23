from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
import datetime

class Feature(Base):
    __tablename__ = "features"
    id = Column(String, primary_key=True)
    asset_id = Column(String, ForeignKey("assets.id"))
    feature_type = Column(String)  # technical, fundamental, whale, derivative
    data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class TechnicalFeature(Base):
    __tablename__ = "technical_features"
    id = Column(String, primary_key=True)
    asset_id = Column(String, ForeignKey("assets.id"))
    rsi_14 = Column(Float)
    macd_line = Column(Float)
    macd_signal = Column(Float)
    macd_histogram = Column(Float)
    ema_20 = Column(Float)
    ema_50 = Column(Float)
    ema_200 = Column(Float)
    sma_20 = Column(Float)
    bollinger_upper = Column(Float)
    bollinger_lower = Column(Float)
    atr_14 = Column(Float)
    obv = Column(Float)
    vwap = Column(Float)
    support_level = Column(Float)
    resistance_level = Column(Float)
    market_regime = Column(String)
    pattern_detected = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class FundamentalFeature(Base):
    __tablename__ = "fundamental_features"
    id = Column(String, primary_key=True)
    asset_id = Column(String, ForeignKey("assets.id"))
    mcap_rank_score = Column(Float)
    volume_mcap_score = Column(Float)
    dev_activity_score = Column(Float)
    community_score = Column(Float)
    tokenomics_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class WhaleFeature(Base):
    __tablename__ = "whale_features"
    id = Column(String, primary_key=True)
    asset_id = Column(String, ForeignKey("assets.id"))
    net_flow_24h = Column(Float)
    exchange_inflow = Column(Float)
    exchange_outflow = Column(Float)
    whale_accumulation = Column(Float)
    large_transactions_count = Column(Integer)
    smart_money_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class DerivativeFeature(Base):
    __tablename__ = "derivative_features"
    id = Column(String, primary_key=True)
    asset_id = Column(String, ForeignKey("assets.id"))
    funding_rate_score = Column(Float)
    open_interest_trend = Column(Float)
    long_short_ratio = Column(Float)
    liquidation_pressure = Column(Float)
    basis_spread = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
