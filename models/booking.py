from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False, index=True)
    from_date = Column(DateTime, nullable=False)
    to_date = Column(DateTime, nullable=False)
    message = Column(Text, nullable=True)
    total_cost = Column(Float, nullable=True)
    status = Column(String(20), default="Pending", nullable=False)  # Pending, Confirmed, Cancelled
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="bookings")
    car = relationship("Car", back_populates="bookings")
