import time
import board
import busio
import RPi.GPIO as GPIO
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from threading import Thread

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=0x48)
ads.gain = 2/3

class AnalogSensor:
    def __init__(self, ads_pin):
        self.int_pin = ads_pin
        self.switch_pin = {1 : ADS.P0,
                           2 : ADS.P1,
                           3 : ADS.P2,
                           4 : ADS.P3}
        self.ads_pin = self.switch_pin[self.int_pin]
        self.channel = AnalogIn(ads, self.ads_pin)

    def _get_value(self):
        return self.channel.value
    
    def _get_voltage(self):
        return self.channel.voltage
    
    def __repr__(self):
        return 'Analog Sensor at' + str(self.int_pin)
    
class O2Sensor(AnalogSensor):
    
    def __init__(self, analogpin):
        super(O2Sensor, self).__init__(ads_pin = analogpin)
        self.current_value = 0
        self.current_voltage = 0
        self.concentration = 0
    
    def _get_concentration(self):
        self.current_voltage = self._get_voltage()
        self.concentration = 0.61051865721074 + 1965.68158984 * self.current_voltage
        return round(self.concentration, 4)
    
    def __repr__(self):
        pass
    
class PressureSensor(AnalogSensor):
    
    def __init__(self, analogpin):
        super(PressureSensor, self).__init__(ads_pin = analogpin)
        self.current_value = 0
        self.current_voltage = 0
        self.pressure = 0
    
    def _get_pressure(self):
        self.current_voltage = self._get_voltage()
        self.pressure = ((self.current_voltage / 5) - 0.04) / 0.0012858
        return round(self.pressure, 4)
    
    def __repr__(self):
        pass

class Valve:
    def __init__(self, valve_relay_pin):
        self.relay_pin = valve_relay_pin
        self.valvepin_gpio = {1 : 26,
                              2 : 21,
                              3 : 20,
                              4 : 16}
        self.pin = self.valvepin_gpio[self.relay_pin]
        self.state = 0
        GPIO.setup(self.pin, GPIO.OUT)
        
    def _open(self):
        self.state = 1
        GPIO.output(self.pin, self.state)
        return
        
    def _close(self):
        self.state = 0
        GPIO.output(self.pin, self.state)
        return
    
    def __repr__(self):
        return 'Valve at pin' + str(self.relay_pin)

if __name__ == "__main__":
    
    # instantiate sensors and valves
    sgx = O2Sensor(1)
    mpx = PressureSensor(3)
    r1 = Valve(1)
    r2 = Valve(2)
    r3 = Valve(3)
    r4 = Valve(4)
    
    def closeall():
        r1._close()
        r2._close()
        r3._close()
        r4._close()
        print('close all')
    def openall():
        r1._open()
        r2._open()
        r3._open()
        r4._open()
        print('open all')
    
        
        
    # set all valves to low
    closeall()
    time.sleep(1)
    openall()
    # time counter
    
    
    # animation part
    x_len = 200
    o2_y_range = [0, 100]
    pressure_y_range = [0, 400]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax1 = ax.twinx()
    ax.set_ylabel("O2 (%)")
    ax1.set_ylabel("Pressure (kPa)")
    plt.xlabel('Sample')
    plt.grid()
    xs = list(range(0, 200))
    ys_o2 = [0] * x_len
    ys_pressure = [0] * x_len
    ax.set_ylim(o2_y_range)
    ax1.set_ylim(pressure_y_range)
    line_o2, = ax.plot(xs, ys_o2, color="r", label="O2")
    line_pressure, = ax1.plot(xs,
                              ys_pressure,
                              color="b",
                              label="Pressure")
    ax.legend(loc="upper left")
    ax1.legend(loc="upper right")
    
    # animation sampling interval
    sampling_interval = 240
    
    # animation functions
    def animate_o2(i, ys_O2):
        current_concentration = sgx._get_concentration()
        ys_O2.append(current_concentration)
        ys_O2 = ys_O2[-x_len:]
        line_o2.set_ydata(ys_O2)
        return line_o2,
    #timing
    is_p1 = False
    is_p2 = False
    is_p3 = False
    is_p4 = False
    
    state_list = [0, 0, 0, 0]
    phase1 = 5
    d_p1_p2 = 5
    d_p2_p3 = 5
    d_p3_p4 = 5
    
    phase2 = phase1 + d_p1_p2
    phase3 = phase2 + d_p2_p3
    phase4 = phase3 + d_p3_p4
    
    totaltime = phase1 + d_p1_p2 + d_p2_p3 + d_p3_p4
    print(phase1, phase2, phase3, phase4)
    print(totaltime)
    
    starttime = int(time.time())
    
    def begin_phase1():
        print("phase1")
        state_list = [1, 0, 0, 0]
        r1._close()
        r2._close()
        r3._close()
        r4._close()
    
    def begin_phase2():
        print("phase1")
        state_list = [0, 1, 0, 0]
        r1._close()
        r2._close()
        r3._open()
        r4._close()
    def begin_phase3():
        print("phase1")
        state_list = [0, 0, 1, 0]
        r1._close()
        r2._open()
        r3._close()
        r4._close()
    def begin_phase4():
        print("phase1")
        state_list = [0, 0, 0, 1]
        r1._close()
        r2._open()
        r3._open()
        r4._close()
    
    def animate_pressure(i, ys_pressure):
        time_int = (int(time.time()) - starttime) % totaltime
        try:
            if 0 <= time_int < phase1:
                begin_phase1()
            elif phase1 <= time_int < phase2:
                begin_phase2()
            elif phase2 <= time_int < phase3:
                begin_phase3()
            elif phase3 <= time_int < phase4:
                begin_phase4()
            print(time_int)
            current_pressure = mpx._get_pressure()
            ys_pressure.append(current_pressure)
            ys_pressure = ys_pressure[-x_len:]
            line_pressure.set_ydata(ys_pressure)
        except OSError:
            i2c = busio.I2C(board.SCL, board.SDA)
            ads = ADS.ADS1115(i2c, address=0x48)
            ads.gain = 2/3
        return line_pressure,
    
    # instantiate animated graphs
    
    animate_o2 = animation.FuncAnimation(fig,
                                         animate_o2,
                                         fargs=(ys_o2, ),
                                         interval=sampling_interval,
                                         blit=False)
    animate_pressure = animation.FuncAnimation(fig,
                                               animate_pressure,
                                               fargs=(ys_pressure, ),
                                               interval=sampling_interval,
                                               blit=False)
    
    plt.show()
