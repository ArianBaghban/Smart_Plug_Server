from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from datetime import datetime

from app.database.connection import Base


class Device(Base):

    __tablename__ = "devices"


    device_id = Column(
        String,
        primary_key=True,
        index=True
    )


    api_key = Column(
        String,
        unique=True,
        nullable=False
    )


    firmware_version = Column(
        String,
        nullable=False
    )


    ip = Column(
        String,
        nullable=True
    )


    uptime = Column(
        Integer,
        nullable=True
    )


    relay = Column(
        Boolean,
        default=False
    )


    last_seen = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    is_online = Column(
        Boolean,
        default=False,
        nullable=False
    )


    last_heartbeat = Column(
        DateTime,
        nullable=True
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )