from mqtt_client import MqttClient
from server import mqtt_config
import signal
import time
import random


def get_random_temperature() -> int:
    return random.randint(0, 100)


def main() -> None:
    client = MqttClient(mqtt_config["host"], mqtt_config["port"], "publisher")

    interrupt_handler = client.get_interrupt_handler()
    signal.signal(signal.SIGINT, interrupt_handler)

    client.connect()
    client.start_publishing()

    while True:
        client.publish_message("status/led", get_random_temperature())
        time.sleep(1)


if __name__ == "__main__":
    main()
