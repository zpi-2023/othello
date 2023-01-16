import uuid
import sys
from connection import ClientConnection, LOCALHOST
from board import Board


def read_client_id() -> str:
    # TODO: read real id from RFID
    return str(uuid.uuid4()).replace("-", "")[:16]


def game_loop(connection: ClientConnection):
    while True:
        message = connection.receive_message()
        match message.tag:
            case "board":
                board = Board.deserialize(message.content)
                image = board.to_image()
                # TODO: draw image on OLED


def main():
    broker_address = sys.argv[1] if len(sys.argv) > 1 else LOCALHOST
    client_id = read_client_id()

    with ClientConnection(broker_address, client_id) as connection:
        game_loop(connection)


if __name__ == "__main__":
    main()
