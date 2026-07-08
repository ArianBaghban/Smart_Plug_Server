from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.database.connection import Base


class DeviceStatus(Base):

    __tablename__ = "device_status"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    device_id = Column(
        String,
        nullable=False
    )

    is_online = Column(
        Boolean,
        nullable=False
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )