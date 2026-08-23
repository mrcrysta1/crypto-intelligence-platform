from sqlalchemy import Column, String, DateTime, Boolean, JSON
from app.models.base import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class UserSettings(Base):
    __tablename__ = "user_settings"
    id = Column(String, primary_key=True)
    user_id = Column(String)
    risk_level = Column(String, default="medium")
    preferred_directions = Column(JSON, default=["LONG", "WATCH"])
    alerts_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
