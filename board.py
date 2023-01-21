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
        # TODO: return only row indices, where there is at least one valid move for color
        return list(range(BOARD_SIZE))

    def tiles_with_valid_move(self, color: Tile, row: int) -> list[int]:
        # TODO: return only tile indices for valid moves
        return list(range(BOARD_SIZE))

    def place(self, row: int, col: int, color: Tile) -> None:
        # TODO: validate move
        self._board[row][col] = color
        # TODO: flip other tiles

    def scores(self) -> dict[Tile, int]:
        # TODO: count placed tiles for each color
        return {Tile.BLACK: 0, Tile.WHITE: 0}

    def winner(self) -> Tile:
        # TODO: check win conditions
        return Tile.EMPTY
