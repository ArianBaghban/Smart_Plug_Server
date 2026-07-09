from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.models.device import Device
from app.models.telemetry import Telemetry
from app.models.command import Command

from app.core.auth import get_current_user


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/devices")
def dashboard_devices(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    devices = db.query(Device).all()

    result = []


    for device in devices:

        last_telemetry = (
            db.query(Telemetry)
            .filter(
                Telemetry.device_id == device.device_id
            )
            .order_by(
                Telemetry.timestamp.desc()
            )
            .first()
        )


        last_command = (
            db.query(Command)
            .filter(
                Command.device_id == device.device_id
            )
            .order_by(
                Command.created_at.desc()
            )
            .first()
        )


        result.append(
            {
                "device_id": device.device_id,
                "is_online": device.is_online,
                "relay": device.relay,
                "ip": device.ip,
                "last_seen": device.last_seen,
                "last_heartbeat": device.last_heartbeat,

                "telemetry": (
                    {
                        "voltage": last_telemetry.voltage,
                        "current": last_telemetry.current,
                        "power": last_telemetry.power,
                        "energy": last_telemetry.energy,
                        "frequency": last_telemetry.frequency,
                        "temperature": last_telemetry.temperature,
                        "wifi_rssi": last_telemetry.wifi_rssi,
                        "timestamp": last_telemetry.timestamp
                    }
                    if last_telemetry
                    else None
                ),

                "last_command": (
                    {
                        "command": last_command.command,
                        "status": last_command.status,
                        "response": last_command.response,
                        "created_at": last_command.created_at,
                        "completed_at": last_command.completed_at
                    }
                    if last_command
                    else None
                )
            }
        )


    return result



@router.get("/commands/{device_id}")
def command_history(
    device_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    commands = (
        db.query(Command)
        .filter(
            Command.device_id == device_id
        )
        .order_by(
            Command.created_at.desc()
        )
        .all()
    )

    return commands



@router.get("/telemetry/{device_id}")
def telemetry_history(
    device_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    telemetry = (
        db.query(Telemetry)
        .filter(
            Telemetry.device_id == device_id
        )
        .order_by(
            Telemetry.timestamp.desc()
        )
        .limit(100)
        .all()
    )

    return telemetry