from datetime import datetime
from pydantic import BaseModel


class DeviceResponse(BaseModel):

    device_id: str
    firmware_version: str
    ip: str | None
    uptime: int | None
    relay: bool
    last_seen: datetime
    is_online: bool
    last_heartbeat: datetime | None

    class Config:
        from_attributes = True