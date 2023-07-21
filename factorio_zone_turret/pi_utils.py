from gpiozero import RGBLED

from colorzero import Color

led = RGBLED(17, 27, 22)


def turn_yellow():
    led.color = Color.from_rgb_bytes(255, 30, 0)


def turn_green():
    led.color = Color.from_rgb_bytes(5, 60, 0)


def turn_red():
    led.color = Color.from_rgb_bytes(255, 0, 0)
