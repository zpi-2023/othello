from typing import Self, Any, Optional
from abc import ABC
import paho.mqtt.client as mqtt
from message import Message

SCOPE_NAME = "othello"
SERVER_UID = "server"


class Connection(ABC):
    def __init__(self, broker_address: str, uid: str) -> None:
        self._broker_address = broker_address
        self._client = mqtt.Client(uid)
        self._uid = uid
        self._message_queue: list[Message] = []

    def __enter__(self) -> Self:
        self._client.on_message = self._on_message
        self._client.connect(self._broker_address)
        self._on_connect()
        self._client.loop_start()
        self._client.subscribe(f"{SCOPE_NAME}/+/{self._uid}/+")
        print(f"[INFO] Connection ({self._uid}) opened!")
        return self

    def __exit__(self, *_) -> None:
        self._client.loop_stop()
        self._on_disconnect()
        self._client.disconnect()
        print(f"[INFO] Connection ({self._uid}) closed!")

    def _on_connect(self) -> None:
        pass

    def _on_disconnect(self) -> None:
        pass

    def _is_message_invalid(self, message: Message) -> bool:
        return False

    def _on_message(self, _client: mqtt.Client, _userdata: Any, data: Any) -> None:
        (scope, sender, receiver, tag) = data.topic.split("/")
        content = str(data.payload.decode("utf-8"))

        if scope != SCOPE_NAME or receiver != self._uid:
            print(f"[WARNING] Dropping invalid topic: {data.topic}")
            return

        message = Message(sender, receiver, tag, content)

        if self._is_message_invalid(message):
            print(f"[WARNING] Dropping invalid message: {message}")
            return

        print(f"[INFO] Received: {message}")

        self._message_queue.append(message)

    def _send_message(self, receiver: str, tag: str, content: Optional[str] = None) -> None:
        self._client.publish(
            "/".join([SCOPE_NAME, self._uid, receiver, tag]),
            content)

    def receive_message(self) -> Message:
        while not any(self._message_queue):
            pass

        return self._message_queue.pop(0)


class ClientConnection(Connection):
    def _on_connect(self) -> None:
        self.send_to_server("connected")

    def _on_disconnect(self) -> None:
        self.send_to_server("disconnected")

    def _is_message_invalid(self, message: Message) -> bool:
        return message.sender != SERVER_UID

    def send_to_server(self, tag: str, content: Optional[str] = None) -> None:
        self._send_message(SERVER_UID, tag, content)


class ServerConnection(Connection):
    def __init__(self, broker_address: str) -> None:
        super().__init__(broker_address, SERVER_UID)

    def _is_message_invalid(self, message: Message) -> bool:
        return message.sender == SERVER_UID
