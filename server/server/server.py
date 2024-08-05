import paho.mqtt.client as mqtt
import time
import random
import signal

mqtt_config = {
    "host": "localhost",
    "port": 1883,
    "topic": "sensor/status",
    "client_id": f"sensor-{random.randint(0, 1000)}",
}

def client_interrupt_handler(client: mqtt.Client):
    def interrupt_handler(signum, frame):
      disconnect_client(client)
      exit(0)
      
    return interrupt_handler

def get_broker_log_info() -> str:
    return f"MQTT Broker at '{mqtt_config["host"]}:{mqtt_config["port"]}'"

def on_connect(client, userdata, flags, reason_code, properties) -> None:
    if reason_code == 0:
        print(
            f"Connected to {get_broker_log_info()}"
        )
    else:
        print(
            f"Failed to connect to {get_broker_log_info()} with return code {reason_code}"
        )

def on_message(client, userdata, msg) -> None:        
  print(f'{msg.topic} {msg.payload}')

def connect_client() -> mqtt:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, mqtt_config["client_id"])
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_config["host"], mqtt_config["port"], 60)

    return client

def start_listening(client: mqtt.Client) -> None:
    print(f"Listening for messages on {get_broker_log_info()} ...")
    client.loop_forever()


def disconnect_client(client: mqtt.Client) -> None:
    print(f"Closing connection to {get_broker_log_info()} ...")
    client.loop_stop()
    print(f"Closed connection to {get_broker_log_info()}")


def main() -> None:
    client = connect_client()
    interrupt_handler = client_interrupt_handler(client)
    signal.signal(signal.SIGINT, interrupt_handler)

    start_listening(client)



if __name__ == "__main__":
    main()
