from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime

from db.database import Base


class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255), nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(50), default="General", nullable=False)  # e.g., Booking, Fleet, Requirements, General
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
