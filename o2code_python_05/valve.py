import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# valves
class Valve:
    def __init__(self, relay_pin, gpio_pin):
        self.relay_pin = relay_pin
        self.gpio_pin = gpio_pin
        self.state = 0
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        
    def _set(self, value):
        GPIO.output(self.gpio_pin, value)
        return
    
    def _open(self):
        GPIO.output(self.gpio_pin, 0)
        return
    
    def _close(self):
        GPIO.output(self.gpio_pin, 1)
        return
    
    def __repr__(self):
        return 'VALVE\nRelay pin:' + str(self.relay_pin) + "\nGPIO pin: " + str(self.gpio_pin)