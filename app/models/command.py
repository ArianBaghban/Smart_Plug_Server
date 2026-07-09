from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.connection import Base


class Command(Base):

    __tablename__ = "commands"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    device_id = Column(
        String,
        nullable=False,
        index=True
    )


    command = Column(
        String,
        nullable=False
    )


    status = Column(
        String,
        default="sent",
        nullable=False
    )


    response = Column(
        String,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    completed_at = Column(
        DateTime,
        nullable=True
    )