from typing import List, Optional
from sqlalchemy import JSON, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base
class Car(Base):
    __tablename__ = 'cars'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_email: Mapped[Optional[str]] = mapped_column(String(160), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    action: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    detailimg: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    avatar: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    date: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    tags: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)

class UserProfile(Base):
    __tablename__ = 'user_profiles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(160), unique=True, index=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    password: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
