from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PageBase(BaseModel):
    page_type: str  # e.g., aboutus, privacy, terms, contactinfo
    title: str
    content: str


class PageCreate(PageBase):
    pass


class PageUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PageResponse(PageBase):
    id: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
