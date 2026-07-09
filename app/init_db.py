from app.database.connection import engine, Base

from app.models.device import Device
from app.models.telemetry import Telemetry
from app.models.user import User
from app.models.device_status import DeviceStatus
from app.models.command import Command


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully")