from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.session import get_db
from app.models.device import Device
from app.core.device_auth import verify_device_key

from app.services.websocket_manager import manager


router = APIRouter(
    prefix="/heartbeat",
    tags=["Heartbeat"]
)


@router.post("/{device_id}")
async def receive_heartbeat(
    device_id: str,
    device: Device = Depends(verify_device_key),
    db: Session = Depends(get_db)
):

    if device.device_id != device_id:
        raise HTTPException(
            status_code=403,
            detail="Device mismatch"
        )


    device.last_heartbeat = datetime.utcnow()
    device.last_seen = datetime.utcnow()
    device.is_online = True


    db.commit()
    db.refresh(device)


    # ارسال وضعیت لحظه‌ای به کلاینت‌های متصل
    await manager.broadcast(
        {
            "event": "device_status",
            "device_id": device.device_id,
            "is_online": device.is_online,
            "last_heartbeat": str(device.last_heartbeat)
        }
    )


    return {
        "message": "Heartbeat received",
        "device_id": device.device_id,
        "is_online": device.is_online,
        "last_heartbeat": device.last_heartbeat
    }