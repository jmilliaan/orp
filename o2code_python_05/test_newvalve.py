from valve import Valve
import time

valve_d = Valve(relay_pin=4, gpio_pin=25)
valve_c = Valve(relay_pin=3, gpio_pin=8)
valve_b = Valve(relay_pin=2, gpio_pin=7)
valve_a = Valve(relay_pin=1, gpio_pin=1)

valve_e = Valve(relay_pin=2, gpio_pin=21)

while True:
    print("Valve A")
    valve_a._open()
    time.sleep(1)
    valve_a._close()
    time.sleep(1)
    
    print("Valve B")
    valve_b._open()
    time.sleep(1)
    valve_b._close()
    time.sleep(1)
    
    print("Valve C")
    valve_c._open()
    time.sleep(1)
    valve_c._close()
    time.sleep(1)
    
    print("Valve D")
    valve_d._open()
    time.sleep(1)
    valve_d._close()
    time.sleep(1)
    
    print("Valve E")
    valve_e._open()
    time.sleep(1)
    valve_e._close()
    time.sleep(1)