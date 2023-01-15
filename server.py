import paho.mqtt.client as mqtt
from message import Message

BROKER = "localhost"

clients = set()


def on_message(_client, _userdata, data):
    msg = Message.parse(data)

    match msg.tag:
        case "connected":
            if len(clients) < 2:
                clients.add(msg.sender)
        case "disconnected":
            clients.discard(msg.sender)


def main():
    server = mqtt.Client("server")
    server.on_message = on_message
    server.connect(BROKER)
    server.loop_start()
    server.subscribe("othello/+/server/+")

    while len(clients) < 2:
        pass

    print(f"Two clients connected: {clients}")

    server.loop_stop()
    server.disconnect()


if __name__ == "__main__":
    main()
