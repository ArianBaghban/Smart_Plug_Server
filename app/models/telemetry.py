from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime

from app.database.connection import Base


class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    device_id = Column(
        String,
        ForeignKey("devices.device_id"),
        nullable=False,
        index=True
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )

    voltage = Column(
        Float,
        nullable=True
    )

    current = Column(
        Float,
        nullable=True
    )

    power = Column(
        Float,
        nullable=True
    )

    energy = Column(
        Float,
        nullable=True
    )

    frequency = Column(
        Float,
        nullable=True
    )

    temperature = Column(
        Float,
        nullable=True
    )

    wifi_rssi = Column(
        Integer,
        nullable=True
    )