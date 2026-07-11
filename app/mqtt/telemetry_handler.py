from datetime import datetime

from app.database.session import SessionLocal
from app.models.device import Device
from app.models.telemetry import Telemetry


def handle_telemetry(data):

    db = SessionLocal()

    try:

        device = (
            db.query(Device)
            .filter(Device.device_id == data["device_id"])
            .first()
        )

        if not device:
            return

        device.last_seen = datetime.utcnow()
        device.is_online = True

        telemetry = Telemetry(
            device_id=data["device_id"],
            timestamp=datetime.utcnow(),
            voltage=data["voltage"],
            current=data["current"],
            power=data["power"],
            energy=data["energy"],
            frequency=data["frequency"],
            temperature=data["temperature"],
            wifi_rssi=data["wifi_rssi"]
        )

        db.add(telemetry)
        db.commit()

    finally:

        db.close()