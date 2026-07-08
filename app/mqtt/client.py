import paho.mqtt.client as mqtt

from app.core.config import settings


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)


def on_connect(client, userdata, flags, reason_code, properties):
    print("MQTT Connected:", reason_code)


def on_message(client, userdata, msg):
    print("MQTT Message Received")
    print("Topic:", msg.topic)
    print("Payload:", msg.payload.decode())


client.on_connect = on_connect
client.on_message = on_message


def connect():
    client.connect(
        settings.MQTT_HOST,
        settings.MQTT_PORT,
        settings.MQTT_KEEPALIVE
    )

    client.loop_start()