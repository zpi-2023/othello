from dataclasses import dataclass
from typing import Any, Optional, Callable
from abc import ABC
from collections import deque
import paho.mqtt.client as mqtt

SCOPE_NAME = "othello"
SERVER_UID = "server"
BROADCAST = "*"
LOCALHOST = "localhost"


@dataclass
class Message:
    sender: str
    receiver: str
    tag: str
    content: str

    @property
    def topic(self) -> str:
        return "/".join([SCOPE_NAME, self.sender, self.receiver, self.tag])

    def __str__(self) -> str:
        return f"({self.sender})->({self.receiver}) [{self.tag}]: \"{self.content}\""


class AbstractChannel(ABC):
    def __init__(self, broker_address: str, uid: str) -> None:
        self._broker_address = broker_address
        self._client = mqtt.Client(uid)
        self._uid = uid
        self._mailbox: deque[Message] = deque()

    def __enter__(self):
        self._client.on_message = self._on_message
        self._client.connect(self._broker_address)
        print(f"[INFO] Connection ({self._uid}) to \"{self._broker_address}\" opened!")
        self._client.loop_start()
        self._client.subscribe(f"{SCOPE_NAME}/+/{self._uid}/+")
        self._client.subscribe(f"{SCOPE_NAME}/+/{BROADCAST}/+")
        self._on_connect()
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

    def _is_message_invalid(self, _message: Message) -> bool:
        return False

    def _on_message(self, _client: mqtt.Client, _userdata: Any, data: Any) -> None:
        (scope, sender, receiver, tag) = data.topic.split("/")
        content = str(data.payload.decode("utf-8"))

        if scope == SCOPE_NAME and sender == self._uid and receiver == BROADCAST:
            return  # Silently drop valid broadcasts from self

        if scope != SCOPE_NAME or sender == self._uid or (receiver != self._uid and receiver != BROADCAST):
            print(f"[WARNING] Dropping invalid topic: {data.topic}")
            return

        message = Message(sender, receiver, tag, content)

        if self._is_message_invalid(message):
            print(f"[WARNING] Dropping invalid message: {message}")
            return

        print(f"[DEBUG] {message}")

        self._mailbox.append(message)

    def _send_message(self, receiver: str, tag: str, content: Optional[str] = None) -> None:
        message = Message(self._uid, receiver, tag, content or '')
        print(f"[DEBUG] {message}")
        self._client.publish(message.topic, message.content)

    def receive_matching(self, condition: Callable[[Message], bool]) -> Message:
        while True:
            for message in self._mailbox:
                if condition(message):
                    self._mailbox.remove(message)
                    return message

    def receive_any(self) -> Message:
        return self.receive_matching(lambda _message: True)


class ClientChannel(AbstractChannel):
    def _on_connect(self) -> None:
        self.send_to_server("connected")

    def _on_disconnect(self) -> None:
        self.send_to_server("disconnected")

    def _is_message_invalid(self, message: Message) -> bool:
        return message.sender != SERVER_UID

    def send_to_server(self, tag: str, content: Optional[str] = None) -> None:
        self._send_message(SERVER_UID, tag, content)


class ServerChannel(AbstractChannel):
    def __init__(self) -> None:
        super().__init__(LOCALHOST, SERVER_UID)

    def send_to_client(self, client_uid: str, tag: str, content: Optional[str] = None) -> None:
        self._send_message(client_uid, tag, content)

    def broadcast(self, tag: str, content: Optional[str] = None) -> None:
        self._send_message(BROADCAST, tag, content)
