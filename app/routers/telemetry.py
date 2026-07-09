from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas.telemetry import TelemetrySchema
from app.database.session import get_db

from app.models.telemetry import Telemetry
from app.models.device import Device

from app.core.device_auth import verify_device_key

from app.services.websocket_manager import manager


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


    # ارسال لحظه‌ای اطلاعات به داشبورد
    await manager.broadcast(
        {
            "event": "telemetry",
            "device_id": telemetry.device_id,
            "voltage": telemetry.voltage,
            "current": telemetry.current,
            "power": telemetry.power,
            "energy": telemetry.energy,
            "frequency": telemetry.frequency,
            "temperature": telemetry.temperature,
            "wifi_rssi": telemetry.wifi_rssi,
            "timestamp": str(telemetry.timestamp)
        }
    )


    return {
        "message": "Telemetry received successfully",
        "device_id": device.device_id,
        "last_seen": device.last_seen
    }