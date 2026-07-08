from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.command import CommandSchema
from app.database.session import get_db
from app.models.device import Device
from app.mqtt.publisher import publish_command

from app.core.auth import get_current_user


router = APIRouter(
    prefix="/commands",
    tags=["Commands"]
)


@router.post("/")
async def send_command(
    command: CommandSchema,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    device = db.query(Device).filter(
        Device.device_id == command.device_id
    ).first()


    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )


    mqtt_result = publish_command(
        device.device_id,
        {
            "command": command.command
        }
    )


    return {
        "message": "Command sent successfully",
        "user": current_user,
        "device_id": device.device_id,
        "command": command.command,
        "mqtt": mqtt_result
    }