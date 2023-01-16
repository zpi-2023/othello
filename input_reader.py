class EncoderReader:
    # TODO: enkoder nie?
    def __init__(self) -> None:
        pass


class ButtonReader:
    # TODO: przycisk tego ten
    def __init__(self, button_color: str) -> None:
        if button_color not in ["green", "red"]:
            raise ValueError("button_color must be 'green' or 'red'")