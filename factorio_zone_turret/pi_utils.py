from gpiozero import LED


def led_on():
    led = LED(17)
    led.on()


def led_off():
    led = LED(17)
    led.off()
