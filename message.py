from dataclasses import dataclass


@dataclass
class Message:
    sender: str
    receiver: str
    tag: str
    content: str

    def __str__(self) -> str:
        return f"({self.sender})->({self.receiver}) [{self.tag}]: \"{self.content}\""
