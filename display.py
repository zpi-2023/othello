from lib.oled.SSD1331 import SSD1331
from PIL import Image


class Display:
    def __init__(self) -> None:
        self._ssd1331 = SSD1331()

    def __enter__(self):
        self._ssd1331.Init()
        self._ssd1331.clear()
        return self

    def __exit__(self, *_) -> None:
        self._ssd1331.clear()

    def draw(self, image: Image) -> None:
        self._ssd1331.ShowImage(image, 0, 0)
