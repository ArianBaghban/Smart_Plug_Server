from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.device import Device


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
async def dashboard_summary(
    db: Session = Depends(get_db)
):

    total_devices = db.query(Device).count()

    online_devices = db.query(Device).filter(
        Device.is_online == True
    ).count()

    offline_devices = total_devices - online_devices

    relay_on = db.query(Device).filter(
        Device.relay == True
    ).count()

    relay_off = total_devices - relay_on


    return {
        "total_devices": total_devices,
        "online_devices": online_devices,
        "offline_devices": offline_devices,
        "relay_on": relay_on,
        "relay_off": relay_off
    }