
import yaml
import time
import threading
from redis_pubsub import publish
import paho.mqtt.client as mqtt
from opcua import Client as OPCClient
from pymodbus.client.sync import ModbusTcpClient

def load_config(path="configs/data_sources.yml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def start_mqtt(config):
    def on_message(client, userdata, msg):
        publish("sensor/stream", {"source": msg.topic, "value": msg.payload.decode()})
    client = mqtt.Client()
    if "username" in config:
        client.username_pw_set(config["username"], config["password"])
    client.on_message = on_message
    client.connect(config["host"], config.get("port", 1883), 60)
    for topic in config["topics"]:
        client.subscribe(topic)
    client.loop_start()

def start_opcua(config):
    client = OPCClient(config["endpoint"])
    client.connect()
    node = client.get_node(config["node_id"])
    class Handler:
        def datachange_notification(self, node, val, data):
            publish("sensor/stream", {"source": str(node), "value": str(val)})
    handler = Handler()
    sub = client.create_subscription(500, handler)
    sub.subscribe_data_change(node)

def start_modbus(config):
    client = ModbusTcpClient(config["host"], port=config.get("port", 502))
    while True:
        rr = client.read_holding_registers(config["register"], 1)
        if rr and rr.registers:
            publish("sensor/stream", {"source": "modbus", "value": rr.registers[0]})
        time.sleep(config.get("interval", 5))

def start_all_ingestors():
    config = load_config()
    for source in config.get("mqtt", []):
        threading.Thread(target=start_mqtt, args=(source,), daemon=True).start()
    for source in config.get("opcua", []):
        threading.Thread(target=start_opcua, args=(source,), daemon=True).start()
    for source in config.get("modbus", []):
        threading.Thread(target=start_modbus, args=(source,), daemon=True).start()
