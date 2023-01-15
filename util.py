def parse_message(data):
    msg = str(data.payload.decode("utf-8"))
    (app, sender, receiver, tag) = data.topic.split("/")
    if app != "othello":
        print(f"[WARNING] Unknown topic detected: {data.topic}")
    print(f"[INFO] From: {sender}; To: {receiver}; Tag: {tag}; Msg: {msg}")
    return sender, tag, msg
