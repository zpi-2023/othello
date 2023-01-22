from config import *
import time

DEBOUNCING_PERIOD_NS = 100_000


class Button:
    """
    Utility wrapper used in previous laboratories, rewritten from C++.
    """

    def __init__(self, pin: int) -> None:
        self._pin = pin

        reading = GPIO.input(pin)
        self._previous_state = reading
        self._debounced_state = reading
        self._last_change_ns = time.monotonic_ns()

        self._was_just_pressed = False
        self._was_just_released = False

    def update(self) -> None:
        """
        Should be called once per tight loop iteration.
        """

        self._was_just_pressed = False
        self._was_just_released = False

        now_ns = time.monotonic_ns()
        reading = GPIO.input(self._pin)

        if self._previous_state != reading:
            self._last_change_ns = now_ns

        if now_ns > self._last_change_ns + DEBOUNCING_PERIOD_NS:
            if self._debounced_state != reading:
                if reading == GPIO.LOW:
                    self._was_just_pressed = True
                elif reading == GPIO.HIGH:
                    self._was_just_released = True
            self._debounced_state = reading

        self._previous_state = reading

    @property
    def is_pressed(self) -> bool:
        return self._debounced_state == GPIO.LOW

    @property
    def is_released(self) -> bool:
        return not self.is_pressed

    @property
    def was_just_pressed(self) -> bool:
        return self._was_just_pressed

    @property
    def was_just_released(self) -> bool:
        return self._was_just_released

    @property
    def was_just_on_edge(self) -> bool:
        return self._was_just_pressed or self._was_just_released


class Encoder:
    """
    Utility wrapper used in previous laboratories, rewritten from C++.
    """

    def __init__(self, first_pin: int, second_pin: int) -> None:
        self._first_button = Button(first_pin)
        self._second_button = Button(second_pin)

        self._was_just_turned_left = False
        self._was_just_turned_right = False

    def update(self) -> None:
        """
        Should be called once per tight loop iteration.
        """

        self._was_just_turned_left = False
        self._was_just_turned_right = False

        self._first_button.update()
        self._second_button.update()

        if self._first_button.was_just_pressed:
            if self._second_button.is_pressed:
                self._was_just_turned_left = True
            else:
                self._was_just_turned_right = True

    @property
    def was_just_turned_left(self) -> bool:
        return self._was_just_turned_left

    @property
    def was_just_turned_right(self) -> bool:
        return self._was_just_turned_right
