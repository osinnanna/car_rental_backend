from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)  # e.g., "High speed. High thrills."
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    cars = relationship("Car", back_populates="category")


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    logo_url = Column(String(500), nullable=True)  # Brand logo as shown in "Top Brands"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    cars = relationship("Car", back_populates="brand", cascade="all, delete-orphan")


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True, index=True)
    title = Column(String(150), nullable=False)
    overview = Column(Text, nullable=True)
    price_per_day = Column(Float, nullable=False)
    fuel_type = Column(String(50), nullable=False)
    model_year = Column(Integer, nullable=False)
    seating_capacity = Column(Integer, nullable=False)
    transmission = Column(String(50), nullable=False, default="Automatic")  # Automatic, Manual
    image_url = Column(String(500), nullable=True)

    # UI Showcase Flags
    is_featured = Column(Boolean, default=False, nullable=False)  # For "Featured Cars" section
    is_slider = Column(Boolean, default=False, nullable=False)    # For Hero "Slide show (of top cars)"

    # Vehicle Features / Accessories
    air_conditioner = Column(Boolean, default=False, nullable=False)
    power_door_locks = Column(Boolean, default=False, nullable=False)
    anti_lock_braking = Column(Boolean, default=False, nullable=False)
    brake_assist = Column(Boolean, default=False, nullable=False)
    power_steering = Column(Boolean, default=False, nullable=False)
    driver_airbag = Column(Boolean, default=False, nullable=False)
    passenger_airbag = Column(Boolean, default=False, nullable=False)
    power_windows = Column(Boolean, default=False, nullable=False)
    cd_player = Column(Boolean, default=False, nullable=False)
    central_locking = Column(Boolean, default=False, nullable=False)
    crash_sensor = Column(Boolean, default=False, nullable=False)
    leather_seats = Column(Boolean, default=False, nullable=False)

    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    brand = relationship("Brand", back_populates="cars")
    category = relationship("Category", back_populates="cars")
    bookings = relationship("Booking", back_populates="car", cascade="all, delete-orphan")
    wishlists = relationship("Wishlist", back_populates="car", cascade="all, delete-orphan")
