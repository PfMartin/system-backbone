import paho.mqtt.client as mqtt_client


class MqttClient:
    def __init__(self, broker_address: str, broker_port: str, client_id: str):
        self.broker_config = {
            "address": broker_address,
            "port": broker_port,
        }
        self.client_id = client_id
        self.broker_info = f"MQTT Broker at {broker_address}:{broker_port}"

    def connect(self) -> None:
        def on_connect(client, userdata, flags, reason_code, properties) -> None:
            if reason_code == 0:
                print(f"Connected to {self.broker_info}")
            else:
                print(
                    f"Failed to connect to {self.broker_info} with return code {reason_code}"
                )

        def on_message(client, userdata, msg) -> None:
            print(f"Received message from topic {msg.topic}: {msg.payload}")

        self.client = mqtt_client.Client(
            mqtt_client.CallbackAPIVersion.VERSION2, self.client_id
        )
        self.client.on_connect = on_connect
        self.client.on_message = on_message

        self.client.connect(self.broker_config["address"], self.broker_config["port"])

    def start_listening(self, topic: str) -> None:
        print(f"Listening for messages on topic '{topic}'")
        self.client.subscribe(topic)
        self.client.loop_forever()

    def start_publishing(self) -> None:
        self.client.loop_start()

    def publish_message(
        self, topic: str, payload: mqtt_client.PayloadType, qos: int = 0
    ) -> None:
        print(f"Publishing message '{payload}' with topic '{topic}'")
        self.client.publish(topic, payload, qos)

    def disconnect(self) -> None:
        print(f"Closing connection to {self.broker_info} ...")
        self.client.loop_stop()
        print(f"Closed connection to {self.broker_info}")

    def get_interrupt_handler(self):
        def interrupt_handler(signum, frame):
            self.disconnect()
            exit(0)

        return interrupt_handler
