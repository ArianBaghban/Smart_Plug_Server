import json

from app.mqtt.manager import mqtt_manager
from app.mqtt.topics import COMMAND_TOPIC


def publish_command(
    device_id: str,
    command: str
):

    topic = COMMAND_TOPIC.format(
        device_id=device_id
    )

    payload = json.dumps({
        "command": command
    })

    mqtt_manager.publish(
        topic,
        payload
    )

    return {
        "topic": topic,
        "payload": payload
    }