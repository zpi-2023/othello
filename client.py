import sys
from config import *
from connection import ClientConnection, LOCALHOST
from board import Board
from lib.oled.SSD1331 import SSD1331
from rfid_reader import RfidReader


def game_loop(connection: ClientConnection, display: SSD1331):
    while True:
        message = connection.receive_message()
        if message.tag == "board":
            board = Board.deserialize(message.content)
            image = board.to_image()
            display.ShowImage(image, 0, 0)


def main():
    display = SSD1331()
    rfid_reader = RfidReader()

    display.Init()
    display.clear()

    broker_address = sys.argv[1] if len(sys.argv) > 1 else LOCALHOST
    
    # TODO: print message that we are waiting for rfid
    print("[INFO] Waiting for rfid card...")
    client_id = rfid_reader.read_uid()

    with ClientConnection(broker_address, client_id) as connection:
        game_loop(connection, display)


if __name__ == "__main__":
    main()
