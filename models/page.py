from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime

from db.database import Base


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    page_type = Column(String(50), unique=True, nullable=False, index=True)  # e.g., aboutus, privacy, terms, contactinfo
    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
