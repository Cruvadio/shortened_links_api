from .database import Base
from datetime import date
from sqlalchemy import Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from pydantic import BaseModel, Field
from typing import Optional
class Link(Base):
    shortened_id: Mapped[str] = mapped_column(String, unique=True)
    original_url: Mapped[str] = mapped_column(String, unique=True)



