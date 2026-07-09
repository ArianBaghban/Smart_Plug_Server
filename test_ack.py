import json
import paho.mqtt.publish as publish


data = {
    "device_id": "P1004",
    "command": "ON",
    "status": "success"
}


publish.single(
    "smartplug/P1004/response",
    json.dumps(data),
    hostname="localhost",
    port=1883
)