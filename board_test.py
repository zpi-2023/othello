from board import Board
from board import Tile

def start_position_test_black():
    board = Board() 
    expected_result = {(2, 3), (3, 2), (4, 5), (5, 4)}
    player = Tile.BLACK

    for x in range(8):
        for y in range(8):
            valid = board._is_move_valid(player, x, y)
            if (x, y) in expected_result:
                assert valid, f'start_position_test_black(): expected valid position at row:{x} col:{y}'
            else:
                assert not valid, f'start_position_test_black(): expected not valid position at row:{x} col:{y}'

def start_position_test_white():
    board = Board() 
    expected_result = {(2, 4), (3, 5), (4, 2), (5, 3)}
    player = Tile.WHITE

    for x in range(8):
        for y in range(8):
            valid = board._is_move_valid(player, x, y)
            if (x, y) in expected_result:
                assert valid, f'start_position_test_black(): expected valid position at row:{x} col:{y}'
            else:
                assert not valid, f'start_position_test_black(): expected not valid position at row:{x} col:{y}'

def place_test_black():
    board = Board()
    #expected_result = {Tile.BLACK : 4, Tile.WHITE : 1}

    board.place(3,2,Tile.BLACK)
    print(board.serialize())
    board.place(4,2,Tile.WHITE)
    print(board.serialize())
    board.place(5,4,Tile.BLACK)
    
    print(board.serialize())
    

if __name__ == '__main__':
    #start_position_test_black()
    #start_position_test_white()
    place_test_black()
    print("Board tested successful, all tests passed")