from time import sleep

from factorio_zone_turret.pi_utils import led_off, led_on

while True:
    led_on()
    sleep(5)
    led_off()
    sleep(5)
