from datetime import datetime
from pydantic import BaseModel


class TelemetrySchema(BaseModel):
    device_id: str

    timestamp: datetime

    voltage: float
    current: float
    power: float
    energy: float
    frequency: float

    temperature: float
    wifi_rssi: int