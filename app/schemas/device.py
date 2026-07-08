from datetime import datetime
from pydantic import BaseModel


class DeviceSchema(BaseModel):
    device_id: str
    firmware_version: str
    timestamp: datetime

    relay: bool

    voltage: float
    current: float
    power: float
    energy: float
    frequency: float

    temperature: float
    wifi_rssi: int

    ip: str
    uptime: int