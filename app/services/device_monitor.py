from datetime import datetime, timedelta
import asyncio

from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.device_status import DeviceStatus
from app.services.websocket_manager import manager


HEARTBEAT_TIMEOUT_MINUTES = 2


def check_offline_devices(db: Session):

    timeout = datetime.utcnow() - timedelta(
        minutes=HEARTBEAT_TIMEOUT_MINUTES
    )

    devices = db.query(Device).all()

    offline_count = 0

    for device in devices:

        if (
            device.last_heartbeat is None
            or device.last_heartbeat < timeout
        ):

            if device.is_online:

                device.is_online = False

                status = DeviceStatus(
                    device_id=device.device_id,
                    is_online=False,
                    timestamp=datetime.utcnow()
                )

                db.add(status)

                asyncio.create_task(
                    manager.broadcast(
                        {
                            "event": "device_status",
                            "device_id": device.device_id,
                            "is_online": False,
                            "timestamp": str(datetime.utcnow())
                        }
                    )
                )

                offline_count += 1

    db.commit()

    return {
        "checked_at": datetime.utcnow(),
        "offline_devices": offline_count
    }