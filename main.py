import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


def square_wave(terms):
    fig = plt.figure()  # type: plt.Figure
    ax = fig.gca()  # type: plt.Axes
    ax.set_xlim(-np.pi, 3 * np.pi)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')

    circlelist = []
    linelist = []

    circlelist.append(plt.Circle((0, 0), 4 / np.pi, fill=0))
    linelist.append(plt.Line2D([0, circlelist[0].radius], [0, 0]))

    ax.add_artist(circlelist[0])
    ax.add_artist(linelist[0])

    for i in range(1, terms):
        n = 2 * i + 1
        x, y = circlelist[i - 1].center
        circlelist.append(plt.Circle((x + circlelist[i - 1].radius, 0), 4 / (n * np.pi), fill=0))
        sum1 = 0

        linelist.append(
            plt.Line2D([x + circlelist[i - 1].radius, circlelist[i - 1].radius + circlelist[i].radius], [0, 0]))
        ax.add_artist(circlelist[i])
        ax.add_artist(linelist[i])

    pencil = plt.Line2D([], [])  # just empty line for now, will update later
    ax.add_artist(pencil)

    steps = 50
    wave_x = np.linspace(np.pi, 3 * np.pi, steps)
    wave_y = np.zeros(steps)
    wave = plt.Line2D(wave_x, wave_y)
    ax.add_artist(wave)
    angles = np.linspace(0, 2 * np.pi, steps)[:steps]

    angles = np.linspace(0, 2 * np.pi, steps + 1)[:steps]

    def update(frame):
        t = angles[frame]  # get the angle

        cx, cy = circlelist[0].center
        r = circlelist[0].radius
        new_x = r * np.cos(t)  # cartesian to polar
        new_y = r * np.sin(t)  # cartesian to polar
        linelist[0].set_data([cx, new_x], [cy, new_y])
        if terms>1:
            for k in range(1, terms):
                circlelist[k].set_center((new_x, new_y))  # update the center of circle2
                r2 = circlelist[k].radius
                new_x2 = new_x + r2 * np.cos((2 * k + 1) * t)  # cartesian to ploar for 2nd term
                new_y2 = new_y + r2 * np.sin((2 * k + 1) * t)  # cartesian to ploar for 2nd term
                linelist[k].set_data([new_x, new_x2], [new_y, new_y2])  # calculate the radius line of circle2
                new_x = new_x2
                new_y = new_y2

            pencil.set_data([new_x2, np.pi], [new_y2, new_y2])
            wave_y[1:] = wave_y[:-1]  # copy every element to the right
            wave_y[0] = new_y2  # add the latest point
            wave.set_ydata(wave_y)
        else:
            pencil.set_data([new_x, np.pi], [new_y, new_y])
            wave_y[1:] = wave_y[:-1]  # copy every element to the right
            wave_y[0] = new_y  # add the latest point
            wave.set_ydata(wave_y)

        return

    anim = animation.FuncAnimation(fig, update, init_func=lambda: None, frames=steps, interval=100)
    plt.show()


if __name__ == '__main__':
    square_wave(3)

