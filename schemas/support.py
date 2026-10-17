from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class FAQBase(BaseModel):
    question: str
    answer: str
    category: str = "General"


class FAQCreate(FAQBase):
    pass


class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None


class FAQResponse(FAQBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SupportQueryRequest(BaseModel):
    query: str


class SupportQueryResponse(BaseModel):
    query: str
    answer: str
    matched_faq: Optional[FAQResponse] = None
    suggestions: List[str] = []
