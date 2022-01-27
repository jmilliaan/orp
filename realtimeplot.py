import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []


def get_light():
    return np.random.randint(255, size=1)[0]


def animate(i, xs, ys):
    data = get_light()
    xs.append(datetime.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(data)
    xs = xs[-20:]
    ys = ys[-20:]
    ax.clear()
    ax.plot(xs, ys)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.grid()
    plt.title('Light Sensor')
    plt.ylabel('Light Intensity')


if __name__ == '__main__':
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
    plt.show()
