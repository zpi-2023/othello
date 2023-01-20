import sys
from netcode import ClientChannel, LOCALHOST
from board import Board, Tile
from rfid_reader import RfidReader
from display import Display


def game_loop(channel: ClientChannel, display: Display):
    board = Board()
    while True:
        message = channel.receive_any()
        if message.tag == "board":
            # TODO: handle deserialization errors
            board = Board.deserialize(message.content)
            display.draw(board.to_image())
            channel.send_to_server("board-ack")
        elif message.tag == "your-turn":
            color = Tile(message.content)
            rows = board.rows_with_valid_moves(color)
            selected_row = next(rows)
            display.draw(board.to_image(selected_row=selected_row))
            # TODO: select row with encoder until button press
            cols = board.tiles_with_valid_move(color, selected_row)
            selected_col = next(cols)
            display.draw(board.to_image(selected_row=selected_row, selected_col=selected_col))
            # TODO: select col with encoder until button press
            channel.send_to_server("place", f"{selected_row},{selected_col}")


def main():
    broker_address = sys.argv[1] if len(sys.argv) > 1 else LOCALHOST

    with Display() as display:
        rfid_reader = RfidReader()
        # TODO: print message that we are waiting for rfid
        print("[INFO] Waiting for RFID card...")
        client_id = rfid_reader.read_uid()

        with ClientChannel(broker_address, client_id) as channel:
            game_loop(channel, display)


if __name__ == "__main__":
    main()
