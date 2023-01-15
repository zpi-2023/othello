import paho.mqtt.client as mqtt
from util import parse_message

broker = "localhost"

clients = set()


def on_message(_client, _userdata, data):
    sender, tag, msg = parse_message(data)

    match tag:
        case "connected":
            if len(clients) < 2:
                clients.add(sender)
        case "disconnected":
            clients.discard(sender)


def main():
    server = mqtt.Client("server")
    server.on_message = on_message
    server.connect(broker)
    server.loop_start()
    server.subscribe("othello/+/server/+")

    while len(clients) < 2:
        pass

    print(f"Two clients connected: {clients}")

    server.loop_stop()
    server.disconnect()


if __name__ == "__main__":
    main()
