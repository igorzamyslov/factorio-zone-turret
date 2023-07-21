from gpiozero import BadPinFactory, RGBLED

from factorio_zone_turret import colors


def _get_mock_led():
    """ Returns mock instance for running the project on a PC and not on Pi """
    from dataclasses import dataclass

    @dataclass
    class MockLED:
        _color: colors.Color = None

        @property
        def color(self):
            return self._color

        @color.setter
        def color(self, value):
            print("Setting LED color to", value)
            self._color = value

        def pulse(self, on_color, **kwargs):
            print("Pulsing LED with color", on_color)

    return MockLED()


try:
    led = RGBLED(17, 27, 22)
except BadPinFactory:
    print("Error: LED not available")
    led = _get_mock_led()


def turn_yellow():
    led.color = colors.YELLOW


def pulse_yellow():
    led.pulse(fade_in_time=.5, fade_out_time=.5,
              on_color=colors.YELLOW, off_color=colors.DARK_YELLOW,
              background=True)


def turn_green():
    led.color = colors.GREEN


def pulse_green():
    led.pulse(fade_in_time=.5, fade_out_time=.5,
              on_color=colors.GREEN, off_color=colors.DARK_GREEN,
              background=True)


def turn_red():
    led.color = colors.RED


def pulse_red():
    led.pulse(fade_in_time=.5, fade_out_time=.5,
              on_color=colors.RED, off_color=colors.DARK_RED,
              background=True)
