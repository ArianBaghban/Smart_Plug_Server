from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.device import Device


def verify_device_key(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):

    device = db.query(Device).filter(
        Device.api_key == x_api_key
    ).first()

    if not device:
        raise HTTPException(
            status_code=401,
            detail="Invalid device api key"
        )

    return device