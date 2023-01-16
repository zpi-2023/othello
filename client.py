import sys
from connection import ClientConnection, LOCALHOST
from board import Board
from rfid_reader import RfidReader


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
    rfid_reader = RfidReader();
    # TODO: print message that we are waiting for rfid
    rfid_reader.wait_for_read();
    client_id = rfid_reader.get_uid();

    with ClientConnection(broker_address, client_id) as connection:
        game_loop(connection)


if __name__ == "__main__":
    main()
