from netcode import ServerChannel
from board import Board, Tile, deserialize_place


def wait_for_players(channel: ServerChannel) -> dict[Tile, str]:
    print("[INFO] Waiting for players...")
    clients: set[str] = set()

    print("0")
    while len(clients) < 2:
        print("1")
        message = channel.receive_any()
        print("2")
        if message.tag == "connected":
            print("3")
            clients.add(message.sender)
        elif message.tag == "disconnected":
            print("4")
            clients.discard(message.sender)
    print("5")

    black_uid = clients.pop()
    white_uid = clients.pop()
    return {Tile.BLACK: black_uid, Tile.WHITE: white_uid}


def game_loop(channel: ServerChannel, players: dict[Tile, str]):
    print("[INFO] Starting the game!")
    board = Board()
    turn = Tile.BLACK

    while board.winner() == Tile.EMPTY:
        messages = channel.flush_mailbox()
        for message in messages:
            if message.tag == "disconnected" and message.sender in players.values:
                print(f"[INFO] Player ({message.sender}) left the game!")
                # TODO: game over, second player wins

        print(f"[INFO] Starting {turn}'s turn!")
        print("[INFO] Sending board state...")
        channel.broadcast("board", board.serialize())
        channel.receive_matching(lambda m: m.sender == players[turn] and m.tag == "board-ack")

        move = None
        while move is None:
            print("[INFO] Waiting for player's move...")
            channel.send_to_client(players[turn], "your-turn", turn.value)
            message = channel.receive_matching(lambda m: m.sender == players[turn] and m.tag == "place")
            move = deserialize_place(message.content)

        row, col = move
        board.place(row, col, turn)

        turn = turn.opposite()


def main():
    print("[INFO] Starting...")
    with ServerChannel() as channel:
        players = wait_for_players(channel)
        game_loop(channel, players)


if __name__ == "__main__":
    main()
