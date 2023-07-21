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


def change_led_color(color: colors.Color):
    led.color = color


def pulse_led(from_color: colors.Color, to_color: colors.Color):
    led.pulse(fade_in_time=.5, fade_out_time=.5,
              on_color=from_color, off_color=to_color,
              background=True)
