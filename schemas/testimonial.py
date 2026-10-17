from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from schemas.user import UserResponse


class TestimonialBase(BaseModel):
    content: str


class TestimonialCreate(TestimonialBase):
    pass


class TestimonialStatusUpdate(BaseModel):
    status: str  # Inactive, Active


class TestimonialResponse(TestimonialBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    user: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)
