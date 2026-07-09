from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.command import CommandSchema
from app.database.session import get_db

from app.models.device import Device
from app.models.command import Command

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

    device = (
        db.query(Device)
        .filter(
            Device.device_id == command.device_id
        )
        .first()
    )


    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )


    if not device.is_online:
        raise HTTPException(
            status_code=400,
            detail="Device is offline"
        )


    new_command = Command(
        device_id=device.device_id,
        command=command.command,
        status="sent"
    )


    db.add(new_command)
    db.commit()
    db.refresh(new_command)


    publish_command(
        device.device_id,
        command.command
    )


    return {
        "message": "Command sent successfully",
        "command_id": new_command.id,
        "device_id": device.device_id,
        "command": command.command,
        "status": new_command.status,
        "user": current_user
    }