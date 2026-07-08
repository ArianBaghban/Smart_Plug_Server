from app.mqtt.client import client


def on_message(client, userdata, msg):
    print("MQTT Message Received")
    print("Topic:", msg.topic)
    print("Payload:", msg.payload.decode())


def start_subscriber(topic: str):
    client.on_message = on_message
    client.subscribe(topic)