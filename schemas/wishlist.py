from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from schemas.car import CarResponse


class WishlistCreate(BaseModel):
    car_id: int


class WishlistResponse(BaseModel):
    id: int
    user_id: int
    car_id: int
    created_at: datetime
    car: Optional[CarResponse] = None

    model_config = ConfigDict(from_attributes=True)
