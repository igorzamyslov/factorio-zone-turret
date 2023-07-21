from gpiozero import Button, RGBLED

from factorio_zone_turret import colors

led = RGBLED(17, 27, 22)
button = Button(2)


def change_led_color(color: colors.Color):
    led.color = color


def pulse_led(from_color: colors.Color, to_color: colors.Color):
    led.pulse(fade_in_time=.5, fade_out_time=.5,
              on_color=from_color, off_color=to_color,
              background=True)
