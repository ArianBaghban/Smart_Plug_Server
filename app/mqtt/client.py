import json
import paho.mqtt.client as mqtt

from app.core.config import settings
from app.mqtt.ack_handler import handle_command_ack


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)


def on_connect(client, userdata, flags, reason_code, properties):

    print("MQTT Connected:", reason_code)

    # دریافت پاسخ دستگاه‌ها
    client.subscribe(
        "smartplug/+/response"
    )



def on_message(client, userdata, msg):

    print("MQTT Message Received")
    print("Topic:", msg.topic)

    payload = msg.payload.decode()

    print("Payload:", payload)


    try:

        data = json.loads(payload)


        if (
            "device_id" in data
            and "command" in data
            and "status" in data
        ):

            handle_command_ack(data)


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