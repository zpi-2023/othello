import uuid
import sys
from connection import ClientConnection, LOCALHOST


def read_client_id() -> str:
    # TODO: read real id from RFID
    return str(uuid.uuid4()).replace("-", "")[:16]


def main():
    broker_address = sys.argv[1] if len(sys.argv) > 1 else LOCALHOST
    client_id = read_client_id()

    with ClientConnection(broker_address, client_id) as connection:
        connection.receive_message()
        # TODO: main game loop


if __name__ == "__main__":
    main()
