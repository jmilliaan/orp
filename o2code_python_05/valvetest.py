from smbus2 import SMBus
import time

offset = 32768
scale = 120

addr = 0x40
cmd = [0x10, 0x00]

with SMBus(1) as bus:
    bus.write_i2c_block_data(addr, 0, cmd)
    time.sleep(0.1)
    block = bus.read_i2c_block_data(addr, 0, 3)
reading = block[0] * 256 + block[1]
crc = block[2]    # should do some crc check for error
flow = (reading - offset)/scale
print(flow)