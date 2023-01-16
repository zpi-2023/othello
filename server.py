from connection import ServerConnection


def main():
    with ServerConnection() as connection:
        clients = set()

        while len(clients) < 2:
            message = connection.receive_message()
            match message.tag:
                case "connected":
                    clients.add(message.sender)
                case "disconnected":
                    clients.discard(message.sender)

        connection.broadcast("game-started")

        # TODO: main game loop


if __name__ == "__main__":
    main()
