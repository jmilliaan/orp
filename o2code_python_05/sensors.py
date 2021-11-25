import board
import busio

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#sensors
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
        return round(self.concentration, 2)
    
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
        return round(self.pressure, 2)
    
    def __repr__(self):
        pass