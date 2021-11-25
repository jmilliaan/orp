import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import o2log
from valve import Valve
import sensors

 #timing
time_offset = 0.01

phase1 = 10 - time_offset
d_p1_p1b = 3 - time_offset
d_p1b_p2 = 5 - time_offset
d_p2_p3 = 10 - time_offset
d_p3_p3b = 3 - time_offset
d_p3b_p4 = 5 - time_offset

phase1b = phase1 + d_p1_p1b
phase2 = phase1b + d_p1b_p2
phase3 = phase2 + d_p2_p3
phase3b = phase3 + d_p3_p3b
phase4 = phase3b + d_p3b_p4

current_phase = 1

cycle_duration = phase1 + d_p1_p1b + d_p1b_p2 + d_p2_p3 + d_p3_p3b + d_p3b_p4
print("Phase Timing:", phase1, phase1b, phase2, phase3, phase3b, phase4)
print("Cycle Duration:", cycle_duration)

# instantiate sensors and valves
sgx = sensors.O2Sensor(1)
mpx = sensors.PressureSensor(3)
mpx2 = sensors.PressureSensor(4)

valve_d = Valve(relay_pin=4, gpio_pin=25)
valve_c = Valve(relay_pin=3, gpio_pin=8)
valve_b = Valve(relay_pin=2, gpio_pin=7)
valve_a = Valve(relay_pin=1, gpio_pin=1)

valve_e = Valve(relay_pin=2, gpio_pin=21)


print(valve_a)
print(valve_b)
print(valve_c)
print(valve_d)
print(valve_e)
# animation part
x_len = 200

o2_y_range = [0, 100]
pressure_y_range = [0, 500]

fig = plt.figure()

ax = fig.add_subplot(1, 1, 1)
ax1 = ax.twinx()
ax2 = ax.twinx()
ax.set_ylabel("O2 (%)")
ax1.set_ylabel("Pressure (kPa)")
ax2.set_ylabel("Pressure (kPa)")

plt.xlabel('Sample')
plt.grid()
xs = list(range(0, 200))

ys_o2 = [0] * x_len
ys_pressure = [0] * x_len
ys_pressure_2 = [0] * x_len

ax.set_ylim(o2_y_range)
ax1.set_ylim(pressure_y_range)
ax2.set_ylim(pressure_y_range)
line_o2, = ax.plot(xs, ys_o2, color="r", label="O2")
line_pressure, = ax1.plot(xs,
                          ys_pressure,
                          color="b",
                          label="Pressure Out")
line_pressure_2, = ax1.plot(xs,
                            ys_pressure_2,
                            color="g",
                            label="Pressure In")
ax.legend(loc="upper left")
ax1.legend(loc="upper right")
ax2.legend(loc="upper right")
sampling_interval = 240

# instantiate logging
data_log = o2log.LogData()


def cycle():
    global current_phase
    
def begin_phase1():
    global current_phase
    current_phase = 1
    
    valve_a._open()
    valve_b._close()
    
    valve_c._close()
    valve_d._open()
    
    valve_e._close()
    
def begin_phase1b():
    global current_phase
    current_phase = "1b"
    
    valve_a._open()
    valve_b._close()
    
    valve_c._close()
    valve_d._open()
    
    valve_e._open()
    
    
def begin_phase2():
    global current_phase
    current_phase = 2
    
    valve_a._close()
    valve_b._open()
    
    valve_c._close()
    valve_d._close()
    
    valve_e._close()
    
    
    
def begin_phase3():
    global current_phase
    current_phase = 3
    
    valve_a._close()
    valve_b._close()
    
    valve_c._open()
    valve_d._close()
    
    valve_e._close()

def begin_phase3b():
    global current_phase
    current_phase = "3b"
    
    valve_a._close()
    valve_b._close()
    
    valve_c._open()
    valve_d._close()
    
    valve_e._open()

    
def begin_phase4():
    global current_phase
    current_phase = 4
    
    valve_a._close()
    valve_b._close()
    
    valve_c._close()
    valve_d._open()
    
    valve_e._close()
    
    
# animation functions
def animate_o2(i, ys_O2):
    
    global current_concentration
    global mpx
    global sgx
    
    try:
        current_concentration = sgx._get_concentration()
        data_log.add_oxygen(current_concentration)
        ys_O2.append(current_concentration)
        ys_O2 = ys_O2[-x_len:]
        line_o2.set_ydata(ys_O2)
        
    except OSError:
        sgx = sensors.O2Sensor(1)
        mpx = sensors.PressureSensor(3)
        
    return line_o2,

def animate_pressure(i, ys_pressure):
    time_int = (int(time.time()) - starttime) % cycle_duration
    
    global current_pressure
    global mpx
    global sgx
    
    try:
        if 0 <= time_int < phase1:
            begin_phase1()
            print("Phase 1", end=" :: ")
            time.sleep(time_offset)
        elif phase1 <= time_int < phase1b:
            begin_phase1b()
            print("Phase 1b", end=" :: ")
            time.sleep(time_offset)
        elif phase1b <= time_int < phase2:
            begin_phase2()
            print("Phase 2", end=" :: ")
            time.sleep(time_offset)
        elif phase2 <= time_int < phase3:
            begin_phase3()
            print("Phase 3", end=" :: ")
            time.sleep(time_offset)
        elif phase3 <= time_int < phase3b:
            begin_phase3b()
            print("Phase 3b", end=" :: ")
            time.sleep(time_offset)
        elif phase3 <= time_int < phase4:
            begin_phase4()
            print("Phase 4", end=" :: ")
            time.sleep(time_offset)
            
        current_pressure = mpx._get_pressure()
        current_pressure_2 = mpx2._get_pressure()
        data_log.add_pressure(current_pressure,
                              current_phase)
        ys_pressure.append(current_pressure)
        ys_pressure = ys_pressure[-x_len:]
        line_pressure.set_ydata(ys_pressure)
        
        currentdata = ("t: " + str(int(time.time()) - starttime) +
                       " :: o2: "+ str(current_concentration) +
                       " :: P out: " + str(current_pressure) +
                       " :: P in : " + str(current_pressure_2))
        
        print(currentdata)
        
        
    except OSError:
        sgx = sensors.O2Sensor(1)
        mpx = sensors.PressureSensor(3)

    return line_pressure,

def animate_pressure_2(i, ys_pressure_2):
    global current_pressure
    global mpx
    global sgx
    
    try:  
        current_pressure_2 = mpx2._get_pressure()
        ys_pressure_2.append(current_pressure_2)
        ys_pressure_2 = ys_pressure_2[-x_len:]
        line_pressure_2.set_ydata(ys_pressure_2)

        
    except OSError:
        sgx = sensors.O2Sensor(1)
        mpx = sensors.PressureSensor(3)

    return line_pressure_2,

def press(event):
    if event.key == 'q':
        try:
            animate_o2.event_source.stop()
            animate_pressure.event_source.stop()
        except AttributeError:
            fig.savefig("plot.png")
            print("Plot saved")

if __name__ == "__main__":
    try:
        starttime = int(time.time())
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
        animate_pressure_2 = animation.FuncAnimation(fig, 
                                                     animate_pressure_2, 
                                                     fargs=(ys_pressure_2, ), 
                                                     interval=sampling_interval, 
                                                     blit=False)
        cid = fig.canvas.mpl_connect('key_press_event', press)
        plt.show()
        
    except:
        pass