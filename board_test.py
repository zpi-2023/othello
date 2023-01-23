from board import Board
from board import Tile

def start_position_test():
    x = Board()
    print(x.rows_with_valid_moves(Tile.BLACK))

if __name__ == '__main__':
    start_position_test()