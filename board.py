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


class Tile(Enum):
    EMPTY = " "
    BLACK = "B"
    WHITE = "W"

    @property
    def image(self) -> Optional[Image.Image]:
        match self:
            case Tile.EMPTY:
                return None
            case Tile.BLACK:
                return BLACK_IMAGE
            case Tile.WHITE:
                return WHITE_IMAGE


class Board:
    def __init__(self) -> None:
        self._board = [
            [Tile.EMPTY for _c in range(BOARD_SIZE)]
            for _r in range(BOARD_SIZE)]
        self._board[3][3] = Tile.WHITE
        self._board[3][4] = Tile.BLACK
        self._board[4][3] = Tile.BLACK
        self._board[4][4] = Tile.WHITE

    def draw(self, /, *, selected_row: Optional[int] = None, selected_col: Optional[int] = None) -> Image.Image:
        image = Image.new("RGBA", BOARD_IMAGE.size)
        image.paste(BOARD_IMAGE)

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                tile_image = self._board[r][c].image
                if tile_image is not None:
                    image.paste(tile_image,
                                (c * TILE_SIZE, r * TILE_SIZE),
                                tile_image)

        if selected_row is not None:
            if selected_col is not None:
                image.paste(SELECTED_TILE_IMAGE,
                            (selected_col * TILE_SIZE, selected_row * TILE_SIZE),
                            SELECTED_TILE_IMAGE)
            else:
                image.paste(SELECTED_ROW_IMAGE,
                            (0, selected_row * TILE_SIZE),
                            SELECTED_ROW_IMAGE)

        return image
