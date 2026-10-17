from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


# Contact Query Schemas
class ContactQueryBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    message: str


class ContactQueryCreate(ContactQueryBase):
    pass


class ContactQueryStatusUpdate(BaseModel):
    status: str  # Pending, Read, Responded


class ContactQueryResponse(ContactQueryBase):
    id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Subscriber Schemas
class SubscriberBase(BaseModel):
    email: EmailStr


class SubscriberCreate(SubscriberBase):
    pass


class SubscriberResponse(SubscriberBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
