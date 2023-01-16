import uuid
from mfrc522 import MFRC522


class RfidReader:
    def __init__(self) -> None:
        self._reader = MFRC522()

    def read_uid(self) -> str:
        while True:
            (status, _) = self._reader.MFRC522_Request(self._reader.PICC_REQIDL)
            if status != self._reader.MI_OK:
                continue

            (status, uid) = self._reader.MFRC522_Anticoll()
            if status != self._reader.MI_OK:
                continue

            return ''.join(uid)

