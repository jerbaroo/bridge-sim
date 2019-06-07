import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation

from model import Bridge, Section


def plot_bridge(b: Bridge):
    """Plot the background of a bridge."""
    plt.hlines(0, 0, b.length, color="green")
    plt.plot(
        np.linspace(0, b.length, len(b.fixed_nodes)),
        [0 for _ in range(len(b.fixed_nodes))],
        "o", color="green")


def plot_section(s: Section):
    """Plot the cross section of a bridge."""
    for p in s.patches:
        plt.plot([p.p0.z, p.p1.z], [p.p0.y, p.p0.y], color="b")  # Bottom.
        plt.plot([p.p0.z, p.p0.z], [p.p0.y, p.p1.y], color="b")  # Left.
        plt.plot([p.p0.z, p.p1.z], [p.p1.y, p.p1.y], color="b")  # Top.
        plt.plot([p.p1.z, p.p1.z], [p.p1.y, p.p0.y], color="b")  # Right.
        dy = abs(p.p0.y - p.p1.y)
        dz = abs(p.p0.z - p.p1.z)
        point = (min(p.p0.y, p.p1.y) + (dy / 2),
                 min(p.p0.z, p.p1.z) + (dz / 2))
        plt.plot(point[1], point[0], "ro")
    plt.show()


def animate_translation(x, y, num_elems=300, node_step=0.2, spans=7):
    """Show an animation of translation of the nodes."""

    def plot_translation(t):
        """Return a plot of model translation at given time index."""
        p = np.arange(0, num_elems * node_step + node_step, node_step)
        plt.ylim(top=np.amax(y), bottom=np.amin(y))
        plot_bridge(num_elems=num_elems, node_step=node_step, spans=spans)
        plt.plot([p[i] + x[t][i] for i in range(len(p))], y[t], color="blue")

    animate_plot(len(x), plot_translation)


def animate_stress_strain(stress_strain, stress=True, num_elems=300,
                          node_step=0.2, spans=7):
    """Show an animation of stress and strain."""
    data = stress_data if stress else strain_data

    def plot_stress_strain(t):
        plt.ylim(top=np.amax(data), bottom=np.amin(data))
        plt.plot(np.arange(0, num_elems * node_step, node_step), data[t],
                 color="blue")
        plot_bridge(num_elems=num_elems, node_step=node_step, spans=spans)

    animate_plot(len(data), plot_stress_strain)


def animate_plot(frames, f):
    """Show an animation with the function f plotting data."""

    def animate(t):
        """Plot at the given time index."""
        plt.cla()
        plt.title(f"time = {t}")
        f(t)

    f(0)
    ani = FuncAnimation(plt.gcf(), animate, frames, interval=1)
    plt.show()
