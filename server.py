from connection import ServerConnection
from board import Board, Tile


def wait_for_players(connection: ServerConnection) -> dict[Tile, str]:
    print("[INFO] Waiting for players...")
    clients: set[str] = set()

    while len(clients) < 2:
        message = connection.receive_message()
        match message.tag:
            case "connected":
                clients.add(message.sender)
            case "disconnected":
                clients.discard(message.sender)

    white_uid = clients.pop()
    black_uid = clients.pop()
    return {Tile.WHITE: white_uid, Tile.BLACK: black_uid}


def game_loop(connection: ServerConnection, players: dict[Tile, str]):
    print("[INFO] Starting the game!")
    board = Board()

    while board.winner() == Tile.EMPTY:
        connection.broadcast("board", board.serialize())

        message = connection.receive_message()
        match message.tag:
            case "disconnected":
                if message.sender in players.values:
                    pass
                    # TODO: game over, second player wins
            case "place":
                pass
                # TODO: place tile on board


def main():
    with ServerConnection() as connection:
        players = wait_for_players(connection)
        game_loop(connection, players)


if __name__ == "__main__":
    main()
