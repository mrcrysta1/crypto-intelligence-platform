from sqlalchemy import Column, String, Float, DateTime, JSON, Boolean
from app.models.base import Base
import datetime

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(String, primary_key=True)
    asset_id = Column(String)
    p_long = Column(Float)
    p_short = Column(Float)
    p_neutral = Column(Float)
    model_version = Column(String)
    features_used = Column(JSON)
    confidence = Column(Float)
    predicted_at = Column(DateTime, default=datetime.datetime.utcnow)

class ModelVersion(Base):
    __tablename__ = "model_versions"
    id = Column(String, primary_key=True)
    version_name = Column(String)
    algorithm = Column(String)
    accuracy = Column(Float)
    precision_score = Column(Float)
    recall_score = Column(Float)
    f1_score = Column(Float)
    training_data_size = Column(Integer)
    trained_at = Column(DateTime)
    is_active = Column(Boolean, default=False)
