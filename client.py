import uuid
from connection import ClientConnection


def main():
    # TODO: read id from RFID
    client_id = str(uuid.uuid4()).replace("-", "")[:16]

    with ClientConnection("localhost", client_id) as connection:
        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
