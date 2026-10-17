from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime

from db.database import Base


class ContactQuery(Base):
    __tablename__ = "contact_queries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False, index=True)
    phone_number = Column(String(20), nullable=True)
    message = Column(Text, nullable=False)
    status = Column(String(20), default="Pending", nullable=False)  # Pending, Read, Responded
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
