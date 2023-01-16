from connection import ServerConnection
from board import Board, Tile


def wait_for_players(connection: ServerConnection) -> None:
    print("[INFO] Waiting for players...")
    clients = set()

    while len(clients) < 2:
        message = connection.receive_message()
        match message.tag:
            case "connected":
                clients.add(message.sender)
            case "disconnected":
                clients.discard(message.sender)


def game_loop(connection: ServerConnection):
    print("[INFO] Starting the game!")
    board = Board()

    while board.winner() == Tile.EMPTY:
        connection.broadcast("board", board.serialize())
        # TODO: wait for player input
        connection.receive_message()


def main():
    with ServerConnection() as connection:
        wait_for_players(connection)
        game_loop(connection)


if __name__ == "__main__":
    main()
