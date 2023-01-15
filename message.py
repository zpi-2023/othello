from dataclasses import dataclass


@dataclass
class Message:
    sender: str
    receiver: str
    tag: str
    content: str

    @staticmethod
    def parse(data):
        content = str(data.payload.decode("utf-8"))
        (app, sender, receiver, tag) = data.topic.split("/")
        if app != "othello":
            print(f"[WARNING] Unknown topic detected: {data.topic}")
        msg = Message(sender, receiver, tag, content)
        print(f"[INFO] {msg}")
        return msg
