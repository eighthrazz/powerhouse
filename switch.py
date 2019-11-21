from gpiozero import LED

class Switch:
    led = None
    status = False

    def __init__(self, pin):
        self.led = LED(pin)
        self.led.off()

    def on(self):
        self.led.on()
        self.status = True

    def off(self):
        self.led.off()
        self.status = False

    def get_status(self):
        return self.status
