from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from schemas.car import CarResponse
from schemas.user import UserResponse


class BookingBase(BaseModel):
    car_id: int
    from_date: datetime
    to_date: datetime
    message: Optional[str] = None


class BookingCreate(BookingBase):
    pass


class BookingStatusUpdate(BaseModel):
    status: str  # Pending, Confirmed, Cancelled


class BookingResponse(BookingBase):
    id: int
    user_id: int
    total_cost: Optional[float] = None
    status: str
    created_at: datetime
    updated_at: datetime
    car: Optional[CarResponse] = None
    user: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)
