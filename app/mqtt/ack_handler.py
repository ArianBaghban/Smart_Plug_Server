from datetime import datetime

from app.database.session import SessionLocal
from app.models.command import Command
from app.models.device import Device


def handle_command_ack(data):

    db = SessionLocal()

    try:

        command = db.query(Command).filter(
            Command.device_id == data["device_id"],
            Command.command == data["command"],
            Command.status == "sent"
        ).first()


        if not command:
            return


        command.status = data["status"]
        command.response = data["status"]
        command.completed_at = datetime.utcnow()


        device = db.query(Device).filter(
            Device.device_id == data["device_id"]
        ).first()


        if device:

            if data["command"] == "ON":
                device.relay = True

            elif data["command"] == "OFF":
                device.relay = False


        db.commit()


    finally:

        db.close()