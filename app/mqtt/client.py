import json
import asyncio

import paho.mqtt.client as mqtt
from datetime import datetime

from app.core.config import settings
from app.mqtt.ack_handler import handle_command_ack
from app.mqtt.telemetry_handler import handle_telemetry

from app.database.session import SessionLocal
from app.models.device import Device

from app.services.websocket_manager import manager


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)


def handle_heartbeat(data):

    db = SessionLocal()

    try:

        device = (
            db.query(Device)
            .filter(
                Device.device_id == data["device_id"]
            )
            .first()
        )

        if not device:
            return

        device.last_heartbeat = datetime.utcnow()
        device.last_seen = datetime.utcnow()
        device.is_online = True

        db.commit()

        asyncio.run(
            manager.broadcast(
                {
                    "event": "device_status",
                    "device_id": device.device_id,
                    "is_online": True,
                    "last_heartbeat": str(device.last_heartbeat)
                }
            )
        )

    finally:

        db.close()



def on_connect(client, userdata, flags, reason_code, properties):

    print("MQTT Connected:", reason_code)

    client.subscribe(
        "smartplug/+/response"
    )

    client.subscribe(
        "smartplug/+/heartbeat"
    )

    client.subscribe(
        "smartplug/+/telemetry"
    )



def on_message(client, userdata, msg):

    print("MQTT Message Received")
    print("Topic:", msg.topic)

    payload = msg.payload.decode()

    print("Payload:", payload)


    try:

        data = json.loads(payload)


        if "heartbeat" in msg.topic:

            handle_heartbeat(data)


        elif "telemetry" in msg.topic:

            handle_telemetry(data)

            asyncio.run(
                manager.broadcast(
                    {
                        "event": "telemetry",
                        **data
                    }
                )
            )


        elif (
            "device_id" in data
            and "command" in data
            and "status" in data
        ):

            handle_command_ack(data)

            asyncio.run(
                manager.broadcast(
                    {
                        "event": "command_ack",
                        "device_id": data["device_id"],
                        "command": data["command"],
                        "status": data["status"]
                    }
                )
            )


    except Exception as e:

        print(
            "MQTT Message Error:",
            e
        )



client.on_connect = on_connect
client.on_message = on_message



def connect():

    client.connect(
        settings.MQTT_HOST,
        settings.MQTT_PORT,
        settings.MQTT_KEEPALIVE
    )

    client.loop_start()