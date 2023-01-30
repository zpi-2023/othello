from netcode import ServerChannel
from board import Board, Tile, deserialize_place


def wait_for_players(channel: ServerChannel) -> dict[Tile, str]:
    print("[INFO] Waiting for players...")
    clients: set[str] = set()

    while len(clients) < 2:
        message = channel.receive_any()
        if message.tag == "connected":
            clients.add(message.sender)
        elif message.tag == "disconnected":
            clients.discard(message.sender)

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
                winner = Tile.WHITE if players[Tile.BLACK] == message.sender else Tile.BLACK
                print(f"[INFO] Game finished, winner: {winner}")
                channel.broadcast("winner", winner.value)
                return

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

    winner = board.winner()
    print(f"[INFO] Game finished, winner: {winner}")
    channel.broadcast("winner", winner.value)


def main():
    print("[INFO] Starting...")
    with ServerChannel() as channel:
        players = wait_for_players(channel)
        game_loop(channel, players)


if __name__ == "__main__":
    main()
