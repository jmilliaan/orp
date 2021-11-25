from valve import Valve
import time

valve_d = Valve(relay_pin=4, gpio_pin=25)
valve_c = Valve(relay_pin=3, gpio_pin=8)
valve_b = Valve(relay_pin=2, gpio_pin=7)
valve_a = Valve(relay_pin=1, gpio_pin=1)

valve_e = Valve(relay_pin=2, gpio_pin=21)

valve_a._open()
valve_b._close()
valve_c._close()
valve_d._close()
time.sleep(1)

while True:
    print("E OPEN")
    valve_e._open()
    time.sleep(2)
    
    print("E CLOSED")
    valve_e._close()
    time.sleep(2)
    