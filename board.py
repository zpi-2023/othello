from __future__ import annotations
import re
from enum import Enum
from typing import Optional
from PIL import Image

BOARD_SIZE = 8
TILE_SIZE = 8
BOARD_IMAGE = Image.open("./img/board.png")
BLACK_IMAGE = Image.open("./img/black.png")
WHITE_IMAGE = Image.open("./img/white.png")
SELECTED_ROW_IMAGE = Image.open("./img/selected-row.png")
SELECTED_TILE_IMAGE = Image.open("./img/selected-tile.png")
BUFFER_PATTERN = re.compile(f"^([BW.]{{{BOARD_SIZE}}}($|\\|)){{{BOARD_SIZE}}}")


def deserialize_place(place_string: str) -> Optional[tuple[int, int]]:
    try:
        rs, _, cs = place_string.partition(",")
        r = int(rs)
        c = int(cs)
        return (r, c)
    except:
        return None


class Tile(Enum):
    EMPTY = "."
    BLACK = "B"
    WHITE = "W"

    @property
    def image(self) -> Optional[Image.Image]:
        if self == Tile.BLACK:
            return BLACK_IMAGE
        elif self == Tile.WHITE:
            return WHITE_IMAGE
        else:
            return None

    def opposite(self) -> Tile:
        if self == Tile.BLACK:
            return Tile.WHITE
        elif self == Tile.WHITE:
            return Tile.BLACK
        else:
            raise ValueError()


class Board:
    def __init__(self) -> None:
        self._board = [[Tile.EMPTY for _c in range(BOARD_SIZE)] for _r in range(BOARD_SIZE)]
        self._board[3][3] = Tile.WHITE
        self._board[3][4] = Tile.BLACK
        self._board[4][3] = Tile.BLACK
        self._board[4][4] = Tile.WHITE

    def to_image(self, /, *, selected_row: Optional[int] = None, selected_col: Optional[int] = None) -> Image.Image:
        image = Image.new("RGBA", BOARD_IMAGE.size)
        image.paste(BOARD_IMAGE)

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                tile_image = self._board[r][c].image
                if tile_image is not None:
                    image.paste(tile_image, (c * TILE_SIZE, r * TILE_SIZE), tile_image)

        if selected_row is not None:
            if selected_col is not None:
                image.paste(SELECTED_TILE_IMAGE,
                            (selected_col * TILE_SIZE, selected_row * TILE_SIZE), SELECTED_TILE_IMAGE)
            else:
                image.paste(SELECTED_ROW_IMAGE, (0, selected_row * TILE_SIZE), SELECTED_ROW_IMAGE)

        # TODO: draw scores and something else in the right panel

        return image.convert("RGB")

    def serialize(self) -> str:
        return "|".join("".join(c.value for c in r) for r in self._board)

    @staticmethod
    def deserialize(buffer: str) -> Optional[Board]:
        if not BUFFER_PATTERN.match(buffer):
            return None

        board = Board()
        for r, tiles in enumerate(buffer.split("|")):
            for c, tile in enumerate(tiles):
                board._board[r][c] = Tile(tile)

        return board

    def rows_with_valid_moves(self, color: Tile) -> list[int]:
        return list(row for row in range(BOARD_SIZE) if self.tiles_with_valid_move(color, row))

    def tiles_with_valid_move(self, color: Tile, row: int) -> list[int]:
        return list(col for col in range(BOARD_SIZE) if self._is_move_valid(color, row, col))

    def _is_move_valid(self, color: Tile, row: int, col: int) -> bool:
        # TODO: validate if the move is legal
        return True

    def place(self, row: int, col: int, color: Tile) -> None:
        # TODO: validate move
        self._board[row][col] = color
        # TODO: flip other tiles

    def scores(self) -> dict[Tile, int]:
        blacks = 0
        whites = 0

        for row in self._board:
            for tile in row:
                if tile == Tile.BLACK:
                    blacks += 1
                elif tile == Tile.WHITE:
                    whites += 1

        return {Tile.BLACK: blacks, Tile.WHITE: whites}

    def winner(self) -> Tile:
        # TODO: check win conditions
        return Tile.EMPTY
