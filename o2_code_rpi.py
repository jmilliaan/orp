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
        return f"Oxygen sensor at pin {self.int_pin}"
    
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
        return f"Pressure Sensor at pin {self.int_pin}"

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

class DataLog:
    def __init__(self):
        self.pressure_list = []
        self.oxygen_list = []
        self.excel_filename = "orp_log.xlsx"
        self.csv_filename = "orp_log.csv"

    def add_data(self, new_p, new_o2):
        self.pressure_list.append(new_p)
        self.oxygen_list.append(new_o2)
    
    def to_excel(self):
        dict_out = {"O2 concentration":self.oxygen_list, 
                    "Pressure":self.pressure_list}
        out_df = pd.DataFrame(dict_out)
        df.to_excel(self.excel_filename)

if __name__ == "__main__":
    try:
        log = DataLog()
        
        # timing
        phase1 = 4
        d_phase1_phase2 = 3
        phase2 = phase1 + d_phase1_phase2 
        
        # instantiate sensors and valves
        sgx = O2Sensor(1)
        mpx = PressureSensor(4)
        
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
        
        # time counter
        global c
        global clock
        clock = 0
        c = time.time()
        
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
            data["o2"].append(current_concentration)
            ys_O2.append(current_concentration)
            ys_O2 = ys_O2[-x_len:]
            line_o2.set_ydata(ys_O2)
            return line_o2,
        
        def animate_pressure(i, ys_pressure):
            global c
            global clock
            
            is_phase1 = False
            is_phase2 = False
            
            current_pressure = mpx._get_pressure()
            data["pressure"].append(current_pressure)
            ys_pressure.append(current_pressure)
            ys_pressure = ys_pressure[-x_len:]
            line_pressure.set_ydata(ys_pressure)
            
            i_c = time.time()
            diff = i_c - c
            c = i_c
            clock += diff
            int_clock = int(clock)
            if int_clock <= phase1:
                if not is_phase1:
                    is_phase1 = True
                    print("phase1")
                    openall()
            if int_clock > phase1 and int_clock <= phase2:
                if not is_phase2:
                    is_phase2 = True
                    print("phase2")
                    closeall()
            if int_clock > phase2:
                print("Cycle done")
                int_clock = 0
                is_phase1 = False
                is_phase2 = False
            print(int_clock)
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
    except KeyboardInterrupt:
        dataset = pd.DataFrame(data)
        filename = str(input("File name (include.xlsx): "))
        dataset.to_excel(filename)
        print("finished")        
