from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas.telemetry import TelemetrySchema
from app.database.session import get_db

from app.models.telemetry import Telemetry
from app.models.device import Device

from app.core.device_auth import verify_device_key


router = APIRouter(
    prefix="/telemetry",
    tags=["Telemetry"]
)


@router.post("/")
async def receive_telemetry(
    data: TelemetrySchema,
    db: Session = Depends(get_db),
    device: Device = Depends(verify_device_key)
):

    if device.device_id != data.device_id:
        raise HTTPException(
            status_code=403,
            detail="Device mismatch"
        )


    device.last_seen = datetime.utcnow()
    device.is_online = True


    telemetry = Telemetry(
        device_id=data.device_id,
        timestamp=data.timestamp,
        voltage=data.voltage,
        current=data.current,
        power=data.power,
        energy=data.energy,
        frequency=data.frequency,
        temperature=data.temperature,
        wifi_rssi=data.wifi_rssi
    )


    db.add(telemetry)

    db.commit()
    db.refresh(telemetry)


    return {
        "message": "Telemetry received successfully",
        "device_id": device.device_id,
        "last_seen": device.last_seen
    }