from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.connection import Base


class RouteModel(Base):
    __tablename__ = "routes"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    interesting_fact: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String(2048))
    location: Mapped[str] = mapped_column(String(120), index=True)
    distance_km: Mapped[float] = mapped_column(Float)
    difficulty: Mapped[str] = mapped_column(String(20), index=True)
    route_type: Mapped[str] = mapped_column(String(30))
    duration_hours: Mapped[int] = mapped_column(Integer)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    altitude_meters: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
