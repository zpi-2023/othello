import paho.mqtt.client as mqtt
import uuid
from util import parse_message

broker = "localhost"


def on_message(_client, _userdata, data):
    sender, tag, msg = parse_message(data)


def main():
    # TODO: read rfid
    client_id = str(uuid.uuid4())

    client = mqtt.Client(client_id)
    client.on_message = on_message
    client.connect(broker)
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
