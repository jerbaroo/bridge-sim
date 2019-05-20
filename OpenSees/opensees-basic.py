import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np

from colorama import init
from matplotlib.animation import FuncAnimation
from termcolor import colored

init()


def print_i(s):
    """Print some info text."""
    print(colored(s, "green"))


def build_model(num_elems=300, node_start=0, node_step=0.2, fix=[], load=[],
                in_file="2018_OpenSees/model-template.tcl",
                out_file="built-model.tcl", elem_out_file="elem.out",
                node_stress_strain_out_file="stress-strain.out",
                node_x_out_file="node-x.out", node_y_out_file="node-y.out"):
    """Build a .tcl file based on the given input."""
    print_i(f"Generating model file with\n\t{num_elems} elements"
            + f"\n\t{node_step} element length")
    with open(in_file) as f:
        in_tcl = f.read()

    out_tcl = in_tcl.replace(
        "<<NODES>>",
        "\n".join(
            f"node {i + 1} {node_step * i + node_start} 0"
            for i in np.arange(num_elems + 1)
        )
    )

    fixed_nodes = np.interp(
        list(map(lambda x: x[0], fix)),
        (0, 1),
        (1, num_elems + 1)
    )
    fixed = ""
    for i in range(len(fix)):
        fixed += f"\nfix {int(fixed_nodes[i])} "
        fixed += f"{fix[i][1]} {fix[i][2]} {fix[i][3]}"
    out_tcl = out_tcl.replace("<<FIX>>", fixed)

    out_tcl = out_tcl.replace(
        "<<ELEMENTS>>",
        "\n".join(
            f"element dispBeamColumn {i + 1} {i + 1} {i + 2} 5 1 1"
            for i in np.arange(num_elems)
        )
    )

    load_nodes = np.interp(
        list(map(lambda x: x[0], load)),
        (0, 1),
        (1, num_elems + 1)
    )
    loads = ""
    for i in range(len(load)):
        loads += f"\nload {int(load_nodes[i])} 0 {load[i][1]} 0"
    out_tcl = out_tcl.replace("<<LOAD>>", loads)

    recorders = ""
    for node_out_file, dof in [(node_x_out_file, 1), (node_y_out_file, 2)]:
        recorders += f"\nrecorder Node -file {node_out_file} -node "
        recorders += " ".join(map(str, np.arange(1, num_elems + 2)))
        recorders += f" -dof {dof} disp"
    recorders += f"\nrecorder Element -file {elem_out_file}"
    recorders += " -ele" + " ".join(map(str, np.arange(1, num_elems + 1)))
    recorders += " globalForce"

    recorders += f"\nrecorder Element -file {node_stress_strain_out_file}"
    recorders += " -ele " + " ".join(map(str, np.arange(1, num_elems + 2)))
    recorders += " section 1 fiber 0 0.5 stressStrain"
    out_tcl = out_tcl.replace("<<RECORDERS>>", recorders)

    with open(out_file, "w") as f:
        f.write(out_tcl)
    print_i(f"Saved model file to {out_file}")


def run_model(model="built-model.tcl",
              node_stress_strain_out_file="stress-strain.out",
              node_x_out_file="node-x.out", node_y_out_file="node-y.out"):
    """Run a model and return the recorded results."""
    print_i(f"Running OpenSees with {model}")
    subprocess.run(["OpenSees", model])
    x = openSeesToNumpy(node_x_out_file)
    y = openSeesToNumpy(node_y_out_file)
    stress_strain = openSeesToNumpy(node_stress_strain_out_file)
    print_i("Read OpenSees recorded data")
    return x, y, stress_strain


def openSeesToNumpy(path):
    """Convert OpenSees output to 2d array."""
    with open(path) as f:
        x = f.read()
    # A string per unit time.
    x = list(filter(lambda y: len(y) > 0, x.split("\n")))
    # A list of string per unit time.
    for i in range(len(x)):
        x[i] = list(map(float, x[i].split()))
    return np.array(x)


def plot_bridge(num_elems=300, node_step=0.2, spans=7):
    """Plot the background of the bridge."""
    stop = num_elems * node_step
    plt.hlines(0, 0, stop, color="green")
    plt.plot(
        np.arange(0, stop + 0.001, stop / spans),
        [0 for _ in range(spans + 1)],
        "o", color="green"
    )


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
    num_t = len(stress_strain)
    num_measurements = len(stress_strain[0]) // 2
    stress_data = [
        [stress_strain[t][i * 2] for i in range(num_measurements)]
        for t in range(num_t)
    ]
    strain_data = [
        [stress_strain[t][i * 2 + 1] for i in range(num_measurements)]
        for t in range(num_t)
    ]
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


if __name__ == "__main__":
    # Degrees of freedom to fix are x, y, rotation.
    build_model(
        fix=[(x, 0, 1, 0) for x in np.arange(0, 1.01, 1/7)],
        load=[(0.5, -5e5), (0.519, -5e5), (0.485, -5e5)]
    )
    x, y, stress_strain = run_model()
    animate_translation(x, y)
    animate_stress_strain(stress_strain)
    animate_stress_strain(stress_strain, stress=False)
