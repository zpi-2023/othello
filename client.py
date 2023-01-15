import paho.mqtt.client as mqtt
import uuid
from message import Message

BROKER = "localhost"


def on_message(_client, _userdata, data):
    msg = Message.parse(data)


def main():
    # TODO: read rfid
    client_id = str(uuid.uuid4())

    client = mqtt.Client(client_id)
    client.on_message = on_message
    client.connect(BROKER)
    client.publish(f"othello/{client_id}/server/connected")
    client.loop_start()
    client.subscribe(f"othello/server/{client_id}/+")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

    client.loop_stop()
    client.publish(f"othello/{client_id}/server/disconnected")
    client.disconnect()


if __name__ == "__main__":
    main()
