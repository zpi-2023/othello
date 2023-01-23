from board import Board
from board import Tile

def test_start():
    x = Board()
    print(x.rows_with_valid_moves(Tile.BLACK))

if __name__ == '__main__':
    test_start()