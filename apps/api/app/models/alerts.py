from sqlalchemy import Column, String, Float, DateTime, JSON, Boolean
from app.models.base import Base
import datetime

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(String, primary_key=True)
    asset_id = Column(String)
    alert_type = Column(String)  # price, signal, whale, score
    condition = Column(JSON)
    is_active = Column(Boolean, default=True)
    message = Column(String)
    last_triggered = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AlertTrigger(Base):
    __tablename__ = "alert_triggers"
    id = Column(String, primary_key=True)
    alert_id = Column(String)
    triggered_at = Column(DateTime, default=datetime.datetime.utcnow)
    trigger_data = Column(JSON)
    notification_sent = Column(Boolean, default=False)
