from app.mqtt.client import client


class DeviceMQTTManager:

    def subscribe_device(self, device_id: str):
        topic = f"smartplug/{device_id}/command"

        result = client.subscribe(topic)

        print("SUBSCRIBE RESULT:", result)
        print("SUBSCRIBED TOPIC:", topic)


device_mqtt_manager = DeviceMQTTManager()