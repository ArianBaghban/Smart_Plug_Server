from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import secrets

from app.schemas.device import DeviceSchema
from app.schemas.device_response import DeviceResponse

from app.database.session import get_db
from app.models.device import Device

from app.mqtt.device_manager import device_mqtt_manager
from app.core.auth import get_current_user


router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.post("/")
async def register_device(
    device: DeviceSchema,
    db: Session = Depends(get_db)
):

    existing_device = db.query(Device).filter(
        Device.device_id == device.device_id
    ).first()


    if existing_device:

        existing_device.firmware_version = device.firmware_version
        existing_device.ip = device.ip
        existing_device.uptime = device.uptime
        existing_device.relay = device.relay
        existing_device.last_seen = datetime.utcnow()

        db.commit()
        db.refresh(existing_device)

        device_mqtt_manager.subscribe_device(
            existing_device.device_id
        )

        return {
            "message": "Device updated successfully",
            "device_id": existing_device.device_id,
            "api_key": existing_device.api_key,
            "last_seen": existing_device.last_seen
        }


    new_device = Device(

        device_id=device.device_id,

        api_key=secrets.token_hex(32),

        firmware_version=device.firmware_version,

        ip=device.ip,

        uptime=device.uptime,

        relay=device.relay,

        last_seen=datetime.utcnow(),

        is_online=False
    )


    db.add(new_device)

    db.commit()

    db.refresh(new_device)


    device_mqtt_manager.subscribe_device(
        new_device.device_id
    )


    return {
        "message": "Device registered successfully",
        "device_id": new_device.device_id,
        "api_key": new_device.api_key,
        "last_seen": new_device.last_seen
    }



@router.get("/", response_model=List[DeviceResponse])
async def get_devices(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    devices = db.query(Device).all()

    return devices