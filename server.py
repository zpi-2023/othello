from connection import ServerConnection
from board import Board, Tile


def wait_for_players(connection: ServerConnection) -> dict[Tile, str]:
    print("[INFO] Waiting for players...")
    clients: set[str] = set()

    while len(clients) < 2:
        message = connection.receive_message()
        if message.tag == "connected":
            clients.add(message.sender)
        elif message.tag == "disconnected":
            clients.discard(message.sender)

    black_uid = clients.pop()
    white_uid = clients.pop()
    return {Tile.BLACK: black_uid, Tile.WHITE: white_uid}


def game_loop(connection: ServerConnection, players: dict[Tile, str]):
    print("[INFO] Starting the game!")
    board = Board()
    turn = Tile.BLACK

    while board.winner() == Tile.EMPTY:
        connection.broadcast("board", board.serialize())
        # TODO: maybe we should send player's color to them before any turns, that would simplify things
        # FIXME: player might be forced to make move before they received the board
        connection.send_to_client(players[turn], "your-turn", turn.value)

        message = connection.receive_message()
        if message.tag == "disconnected" and message.sender in players.values:
            pass  # TODO: game over, second player wins
        elif message.tag == "place":
            pass  # TODO: place tile on board


def main():
    with ServerConnection() as connection:
        players = wait_for_players(connection)
        game_loop(connection, players)


if __name__ == "__main__":
    main()
