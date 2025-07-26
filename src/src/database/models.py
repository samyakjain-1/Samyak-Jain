from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    hypothesis = Column(String, index=True)
    summary = Column(String)
    confidence_score = Column(Float)
    recommendation = Column(String)
    confirmations = Column(JSON)
    contradictions = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, index=True)
    type = Column(String)
    message = Column(String)
    priority = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
