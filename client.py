import sys
from connection import ClientConnection, LOCALHOST
from board import Board
from rfid_reader import RfidReader
from display import Display


def game_loop(connection: ClientConnection, display: Display):
    while True:
        message = connection.receive_message()
        if message.tag == "board":
            board = Board.deserialize(message.content)
            image = board.to_image()
            display.draw(image)


def main():
    broker_address = sys.argv[1] if len(sys.argv) > 1 else LOCALHOST

    with Display() as display:
        rfid_reader = RfidReader()
        # TODO: print message that we are waiting for rfid
        print("[INFO] Waiting for rfid card...")
        client_id = rfid_reader.read_uid()

        with ClientConnection(broker_address, client_id) as connection:
            game_loop(connection, display)


if __name__ == "__main__":
    main()
