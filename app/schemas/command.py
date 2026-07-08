from pydantic import BaseModel

class CommandSchema(BaseModel):
    device_id: str
    command: str