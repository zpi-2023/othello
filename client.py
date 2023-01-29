import sys
import time
from typing import Any, Callable, Optional
from PIL import Image
from config import *
from netcode import ClientChannel, LOCALHOST
from board import Board, Tile
from rfid_reader import RfidReader
from input_reader import Button, Encoder
from display import Display

RFID_IMAGE = Image.open("./img/rfid.png").convert("RGB")
WAITING_PLAYER_IMAGE = Image.open("./img/waiting-player.png").convert("RGB")
WIN_BLACK = Image.open("./img/win-black.png").convert("RGB")
WIN_WHITE = Image.open("./img/win-white.png").convert("RGB")

button_red = Button(button_red_pin)
button_green = Button(button_green_pin)
encoder = Encoder(encoder_first_pin, encoder_second_pin)


def buzzer(state: bool) -> None:
    GPIO.output(buzzer_pin, not state)


def select_with_encoder(
        choices: list[Any],
        on_selection: Callable[[Any],
                               None],
        can_cancel: bool = False) -> Optional[Any]:
    selected_index = 0
    on_selection(choices[selected_index])
    print("[INFO] Waiting for user input...")
    while True:
        button_red.update()
        button_green.update()
        encoder.update()

        if encoder.was_just_turned_left:
            selected_index = (selected_index - 1) % len(choices)
            on_selection(choices[selected_index])

        if encoder.was_just_turned_right:
            selected_index = (selected_index + 1) % len(choices)
            on_selection(choices[selected_index])

        if button_red.was_just_pressed:
            return choices[selected_index]

        if can_cancel and button_green.was_just_pressed:
            return None


def game_loop(channel: ClientChannel, display: Display):
    board = Board()
    while True:
        message = channel.receive_any()
        if message.tag == "board":
            print("[INFO] Received new board.")
            new_board = Board.deserialize(message.content)
            if new_board is not None:
                board = new_board
                display.draw(board.to_image())
                channel.send_to_server("board-ack")
            else:
                print("[WARNING] Invalid board received!")
        elif message.tag == "your-turn":
            print("[INFO] Your turn!")
            color = Tile(message.content)
            display.draw(board.to_image(color=color))

            selected_row = None
            selected_col = None
            while selected_col is None:
                print("[INFO] Select row...")
                valid_rows = board.rows_with_valid_moves(color)
                selected_row = select_with_encoder(
                    valid_rows,
                    lambda row: display.draw(board.to_image(row, color=color)),
                    can_cancel=False
                )
                print("[INFO] Select column...")
                valid_cols = board.tiles_with_valid_move(color, selected_row)
                selected_col = select_with_encoder(
                    valid_cols,
                    lambda col: display.draw(board.to_image(selected_row, col, color=color)),
                    can_cancel=True
                )

            print("[INFO] Placing tile...")
            channel.send_to_server("place", f"{selected_row},{selected_col}")
        elif message.tag == "winner":
            winner = Tile(message.content)
            print(f"[INFO] Game finished, winner: {winner}")
            if winner == Tile.BLACK:
                display.draw(WIN_BLACK)
            elif winner == Tile.WHITE:
                display.draw(WIN_WHITE)
            else:
                print(f"[WARNING] Invalid winner: {winner}")


def main():
    print("[INFO] Starting...")
    broker_address = sys.argv[1] if len(sys.argv) > 1 else LOCALHOST

    with Display() as display:
        rfid_reader = RfidReader()
        display.draw(RFID_IMAGE)
        print("[INFO] Waiting for RFID card...")
        client_id = rfid_reader.read_uid()
        print("[INFO] RFID scanned, waiting for other player...")
        buzzer(True)
        display.draw(WAITING_PLAYER_IMAGE)
        time.sleep(1)
        buzzer(False)

        with ClientChannel(broker_address, client_id) as channel:
            game_loop(channel, display)


if __name__ == "__main__":
    main()
