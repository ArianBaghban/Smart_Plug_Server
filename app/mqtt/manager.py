from app.mqtt.client import client, connect
from app.mqtt.subscriber import start_subscriber


class MQTTManager:

    def start(self):
        connect()

    def publish(self, topic: str, payload: str):
        client.publish(topic, payload)

    def subscribe(self, topic: str):
        start_subscriber(topic)


mqtt_manager = MQTTManager()