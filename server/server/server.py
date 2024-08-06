import time
import random
import signal
from mqtt_client import MqttClient

mqtt_config = {
    "host": "localhost",
    "port": 1883,
    "topic": "sensor/status",
    "client_id": "server",
}


def main() -> None:
    client = MqttClient(
        mqtt_config["host"], mqtt_config["port"], mqtt_config["client_id"]
    )

    interrupt_handler = client.get_interrupt_handler()
    signal.signal(signal.SIGINT, interrupt_handler)

    client.connect()
    client.start_listening("status/led")


if __name__ == "__main__":
    main()
