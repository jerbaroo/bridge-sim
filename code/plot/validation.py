import itertools
from collections import defaultdict
from typing import Dict, List

import matplotlib
import numpy as np
import pandas as pd

from config import Config
from fem.responses import Responses
from model.bridge import Point
from plot import plt
from util import print_i, scalar


def plot_mmm_strain_convergence(
    c: Config, pier: int, parameters: pd.DataFrame, all_strains: Dict[float, Responses]
):
    """Plot convergence of given responses as model size grows."""
    # A grid of points 1m apart, over which to calculate responses.
    grid = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, int(c.bridge.length)),
            np.linspace(c.bridge.z_min, c.bridge.z_max, int(c.bridge.width)),
        )
    ]
    # Collect responses over all responses, and over the grid.
    mins, maxes, means = [], [], []
    gmins, gmaxes, gmeans = [], [], []
    num_sims = len(list(all_strains))
    for sim, strains in enumerate(all_strains.values()):
        print_i(f"Gathering strains from simulation {sim + 1} / {num_sims}", end="\r")
        grid_strains = np.array([strains.at_deck(point, interp=True) for point in grid])
        gmins.append(scalar(np.min(grid_strains)))
        gmaxes.append(scalar(np.max(grid_strains)))
        gmeans.append(scalar(np.mean(grid_strains)))
        strains = np.array(list(strains.values()))
        mins.append(scalar(np.min(strains)))
        maxes.append(scalar(np.max(strains)))
        means.append(scalar(np.mean(strains)))
    print()
    max_shell_lens = list(all_strains.keys())
    plt.plot(max_shell_lens, mins, label="mins")
    plt.plot(max_shell_lens, maxes, label="maxes")
    plt.plot(max_shell_lens, means, label="means")
    plt.plot(max_shell_lens, gmins, label="gmins")
    plt.plot(max_shell_lens, gmaxes, label="gmaxes")
    plt.plot(max_shell_lens, gmeans, label="gmeans")
    plt.legend()
    plt.landscape()
    plt.xlim(plt.xlim()[1], plt.xlim()[0])
    plt.tight_layout()
    plt.savefig(c.get_image_path("convergence-pier-strain", "mmm.pdf"))
    plt.close()


def plot_nesw_convergence(
        c: Config,
        responses: Dict[float, Responses],
        point: Point,
        max_distance: float,
):
    """Plot convergence of strain at different points around a load."""
    delta_distance = 0.01
    skip = 3
    # Create color mappable for distances.
    norm = matplotlib.colors.Normalize(vmin=0, vmax=max_distance)
    cmap = matplotlib.cm.get_cmap("jet")
    mappable = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
    color = lambda d: mappable.to_rgba(d)
    # For each compass point.
    compass_dir = {
        "N": (0, 1),
        "E": (-1, 0),
        "S": (0, -1),
        "W": (1, 0),
    }
    plt.square()
    fig, axes = plt.subplots(nrows=2, ncols=2)
    for ax, compass, compass_name, in zip(
        axes.flat, ["N", "S", "E", "W"], ["North", "South", "East", "West"]
    ):
        # Collect data into responses.
        x_mul, z_mul = compass_dir[compass]
        for distance in np.arange(0, max_distance, step=delta_distance)[::skip]:
            dist_point = Point(
                x=point.x + (distance * x_mul),
                y=point.y,
                z=point.z + (distance * z_mul),
            )
            print(dist_point)
            if (
                dist_point.x < c.bridge.x_min
                or dist_point.x > c.bridge.x_max
                or dist_point.z < c.bridge.z_min
                or dist_point.z > c.bridge.z_max
            ):
                break
            line_responses = []
            for max_shell_len, sim_responses in responses.items():
                line_responses.append((
                    max_shell_len,
                    scalar(sim_responses.at_deck(dist_point, interp=True))
                ))
            line_responses = np.array(sorted(line_responses, key=lambda t: t[0])).T
            ax.plot(line_responses[0], line_responses[1], color=color(distance))
            if distance > max_distance:
                break
        ax.set_xlim(ax.get_xlim()[1], ax.get_xlim()[0])
        ax.set_title(
            f"Strain at increasing distance\nin direction {compass_name}"
        )
        ax.set_xlabel("max_shell_len (m)")
        ax.set_ylabel("Strain (m\m)")
    plt.tight_layout()
    clb = plt.colorbar(mappable, ax=axes.ravel())
    clb.ax.set_title("Distance (m)")
